
from nineml.utility import invert_dictionary,flatten_first_level, expect_single

# System Imports:
import copy
import itertools


import nineml.abstraction_layer as al
from nineml.abstraction_layer.visitors import ClonerVisitor, ClonerVisitorPrefixNamespace

class ComponentFlattener(object):
    
    @classmethod
    def flatten_namespace(cls, ns):
        return ns.replace('.','_')
    
    @classmethod
    def flatten_namespace_dict(cls, ns):
        newParams = {}
        for k,v in ns.iteritems():
            newParams[ cls.flatten_namespace(k) ] = v
        return newParams
     
    
    
    



    def __init__(self,model, componentname=None):
        assert isinstance( model, al.ComponentClass)

        # Is our component already flat??
        if model.is_flat():
            self.reducedcomponent = ClonerVisitor.visit( model )
            return

        # New components name
        self.componentname=componentname if componentname else model.name


        # Flatten all the namespaces:
        self.model = ClonerVisitorPrefixNamespace().visit(model)

        # Make a list of all components, and those components with regimes: 
        self.all_components = list( self.model.query.recurse_all_components )
        self.componentswithregimes = [ m for m in self.all_components if list(m.regimes) ] 
        
        
        self.build_new_regime_space()
        self.remap_ports()






    def create_compound_regime( self, regimetuple, index ):
        
        # Copy accross all the odes from each regime. 
        # [Don't worry about transitions yet, we deal with them later]

        # We need to clone the time_derivatives:
        time_derivatives = flatten_first_level( [ r.time_derivatives for r in regimetuple ] )
        time_derivatives = [ ClonerVisitor().visit(td) for td in time_derivatives ]

        return al.Regime( name=None, 
                        time_derivatives = time_derivatives,
                        on_events=[], 
                        on_conditions=[] )


        



    def create_new_transition( self, oldtransition, regimetuple, regimeIndex,
            regimeNew, newRegimeLookupMap, event_port_map ):
                # Clone the node:
                oldtransition = oldtransition.accept_visitor( ClonerVisitor(), prefix='', prefix_excludes=[] )


                handled_events = []
                unhandled_events = []

                state_assignments = oldtransition.state_assignments
                output_events = oldtransition.event_outputs
                unhandled_events.extend( flatten_first_level(
                    [self.distribute_event( ev, event_port_map) for ev in output_events ]) ) 

                newRegimeTuple = self.getNewRegimeTupleFromTransition( currentRegimeTuple = regimetuple, regimeIndex=regimeIndex, oldtransition=oldtransition)
                
                while unhandled_events:
                    ev = unhandled_events.pop()
                    new_state_assignments, new_event_outputs, newRegimeTuple = self.getRegimeTupleResponseToEvent(newRegimeTuple, ev ) 
                    
                    # Check for event recursion:
                    for new_ev in new_event_outputs: assert not new_ev in handled_events and new_ev != ev
                    
                    state_assignments.extend( new_state_assignments )
                    output_events.extend( new_event_outputs )
                    unhandled_events.extend( flatten_first_level(
                        self.distribute_event( new_event_outputs, event_port_map ) ) )
                    handled_events.append(ev)

                

                targetRegime = newRegimeLookupMap[ newRegimeTuple ]

                return state_assignments, output_events, targetRegime.name

                newOnCondition = al.OnCondition(oldtransition.trigger, state_assignments=state_assignments, event_outputs = output_events, target_regime_name = targetRegime.name)
                regimeNew.add_on_condition( newOnCondition)

    def distribute_event(self, event_output, event_port_map):
        print 'Distributing Event', event_output, event_output.port_name
        events = set()
        for p1,p2 in event_port_map:
            if p1 == event_output.port_name:
                events.append( p2 )
                events = events + self.distribute_event(p2)
        return events



    def getRegimeTupleResponseToEvent( self, regimeTuple, eventName ):
        " Do not recurse, but iterate once over each regime in the tuple"

        state_assignments = []
        event_outputs = []
        newRegimeTuple = list( regimeTuple )

        for index,regime in enumerate(regimeTuple):
            on_events = [ oe for oe in regime.on_events if oe.src_port_name == eventName ] 
            assert len(on_events) in [0,1]
            if not on_events: continue

            on_event = on_events[0]
            state_assignments.extend( [sa.accept_visitor( ClonerVisitor() ) for sa in on_event.state_assignments ]) 
            event_outputs.extend( [eo.accept_visitor( ClonerVisitor() ) for eo in one_event.event_outputs ]) 
            
            #Update dstRegime
            dstRegimeName = oldtransition.to.get_ref() if oldtransition.to else regime
            dstRegime = self.componentswithregimes[regimeIndex].query.regime(name=dstRegimeName.name) 
            newRegimeTuple[index] = dstRegime

        return state_assignments, event_outputs, tuple( newRegimeTuple )
    

    def getNewRegimeTupleFromTransition( self,currentRegimeTuple, regimeIndex, oldtransition ):
            srcRegime = list( currentRegimeTuple )
            dstRegimeTuple = srcRegime[:]

            # Points to another node:
            name = oldtransition.target_regime_name
            dstRegimeOld = self.componentswithregimes[regimeIndex].query.regime(name=name) 
            dstRegimeTuple[regimeIndex] = dstRegimeOld

            #print 'New Regime Transition:', currentRegimeTuple, '->', tuple( dstRegimeTuple )
            return tuple(dstRegimeTuple)



    def build_new_regime_space(self):

        newRegimeLookupMap = {}
        regimes = [ comp.regimes for comp in self.componentswithregimes]
        for i,regimetuple in enumerate( itertools.product(*regimes) ):
            newRegime = self.create_compound_regime( regimetuple, i ) 
            newRegimeLookupMap[regimetuple] = newRegime

        

        # Check for event-emission cycles:
        # TODO
        recv_event_input_ports = flatten_first_level( [comp.query.event_recv_ports() for comp in self.all_components] )
        event_port_map = flatten_first_level( [comp.query.get_fully_qualified_port_connections() for comp in self.all_components] )
        event_port_map = [ (p1.getstr(), p2.getstr() ) for (p1,p2) in event_port_map ] 





        for regimetuple,regimeNew in newRegimeLookupMap.iteritems():

            for regimeIndex, regime in enumerate( regimetuple ):
                print 'Regime Index:',regimeIndex
                
                # Lets see what happens if we get events. The simple case is just changing the
                
                for oldtransition in regime.on_conditions:

                    res = self.create_new_transition(
                            oldtransition=oldtransition,
                            regimetuple=regimetuple, regimeIndex=regimeIndex,
                            regimeNew=regimeNew,
                            newRegimeLookupMap=newRegimeLookupMap,
                            event_port_map=event_port_map)

                    state_assignments, output_events, target_regime_name = res
                    newOnCondition = al.OnCondition(oldtransition.trigger, state_assignments=state_assignments, event_outputs = output_events, target_regime_name = target_regime_name)
                    regimeNew.add_on_condition( newOnCondition)

                for oldtransition in regime.on_events:
                    res = self.create_new_transition(
                            oldtransition=oldtransition,
                            regimetuple=regimetuple, regimeIndex=regimeIndex,
                            regimeNew=regimeNew,
                            newRegimeLookupMap=newRegimeLookupMap,
                            event_port_map=event_port_map)

                    state_assignments, output_events, target_regime_name = res
                    newOnCondition = al.OnEvent(oldtransition.src_port_name, state_assignments=state_assignments, event_outputs = output_events, target_regime_name = target_regime_name)
                    regimeNew.add_on_event( newOnCondition)
                    
        self.newRegimeLookupMap = newRegimeLookupMap
                



    







    def remap_ports(self):
        from nineml.utility import safe_dictionary_merge
        newRegimeLookupMap = self.newRegimeLookupMap

        from nineml.utility import flatten_first_level
        from nineml.abstraction_layer.component import NamespaceAddress, ComponentClass

        new_analog_ports = flatten_first_level( [comp.analog_ports for comp in self.all_components]) 
        new_analog_ports = dict( [ (p.name, p) for p in new_analog_ports ] ) 
        



        from nineml.utility import flatten_first_level
        #from nineml.abstraction_layer import ComponentClass

        print 'Regimes:', newRegimeLookupMap.values()
        dynamics = al.Dynamics( regimes = newRegimeLookupMap.values(),
                                aliases = flatten_first_level( [ m.aliases for m in self.all_components ] ),
                                state_variables = flatten_first_level( [ m.state_variables for m in self.all_components ]  ),
                                )  


        #Remap the event-ports:
        

        self.reducedcomponent = al.ComponentClass( name=self.componentname, 
                                                         dynamics=dynamics, 
                                                         analog_ports=new_analog_ports.values() , 
                                                         event_ports= flatten_first_level( [comp.event_ports for comp in self.all_components] ), 
                                                         parameters=flatten_first_level( [ m.parameters for m in self.all_components ] ) )








        # Remap Ports:
        def globalRemapPort(originalname,targetname):
            print 'Global-Remap [%s -> %s]'%(originalname,targetname)
            from nineml.abstraction_layer.visitors import ExpandPortDefinition
            transform = ExpandPortDefinition( originalname=originalname, targetname=targetname)

            self.reducedcomponent.accept_visitor(transform)



        
        # Handle port mappings:
        # portconnections = [ (NS -> NS),(NS -> NS ), (NS -> NS) ]
        #portconnections = [model.query.get_fully_qualified_port_connections() for model in self.all_components] 
        portconnections = [model.portconnections for model in self.all_components]
        portconnections = list( itertools.chain(* portconnections ) )
        
        print portconnections

        # A. Handle Recieve Ports:
        for srcAddr,dstAddr in portconnections[:]:
            srcPort = new_analog_ports[srcAddr.loctuple[-1] ]
            dstPort = new_analog_ports[dstAddr.loctuple[-1]]
            if dstPort.mode == 'recv':
                globalRemapPort( dstPort.name, srcPort.name )
                
                del new_analog_ports[ dstAddr.loctuple[-1] ]
                self.reducedcomponent._analog_ports.remove( expect_single([p for p in self.reducedcomponent.analog_ports if p.name == dstAddr.loctuple[-1] ]) )

                portconnections.remove( (srcAddr,dstAddr) )

        # B. Handle Reduce Ports:
        # 1/ Make a map { reduce_port -> [send_port1, send_port2, send_port3], ...}
        from collections import defaultdict
        reduce_connections = defaultdict( list )
        for src,dst in portconnections:
            dstport = new_analog_ports[dst.loctuple[-1] ]
            srcport = new_analog_ports[src.loctuple[-1] ]
            if dstport.mode == 'reduce':
                reduce_connections[dstport].append(srcport)

        # 2/ Subsitute each reduce port in turn:
        for dstport, srcportList in reduce_connections.iteritems():
            src_subs = [ s.name for s in srcportList ]
            terms = [dstport.name] + src_subs
            reduce_expr= dstport.reduce_op.join(terms) 
            globalRemapPort( dstport.name, reduce_expr )



def flatten( model, componentname=None ):
    reducer = ComponentFlattener(model,componentname)
    return reducer.reducedcomponent

