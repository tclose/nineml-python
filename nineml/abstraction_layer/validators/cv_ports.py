import nineml.abstraction_layer as al
from nineml.abstraction_layer.visitors import InplaceActionVisitorDF
from nineml.utility import *
from itertools import chain

from collections import defaultdict
from nineml.abstraction_layer.validators.base import ComponentValidatorPerNamespace


# Check that the sub-components stored are all of the
# right types:
#class ComponentValidatorPortNames(InplaceActionVisitorDF):
#    """Checks that we only have a single port of each name""" 
#    def __init__(self, component):
#        InplaceActionVisitorDF.__init__(self, explicitly_require_action_overrides=False)
#        
#        self.recv_event_ports = []
#        self.send_event_ports = []
#        self.recv_analog_ports = []
#        self.send_analog_ports = []
#        
#        self.visit(component)
#
#
#    def action_componentclass(self, component):
#        assert isinstance( component, al.ComponentClass )
#        
#        # Check for name duplication:
#        portNames = [ p.name for p in chain( component.event_ports, component.analog_ports )] 
#        assert_no_duplicates(portNames)
#
#        self.recv_event_port_names = [ p.name for p in component.event_ports if p.mode=='recv']
#        self.send_event_port_names = [ p.name for p in component.event_ports if p.mode=='send']
#        self.recv_analog_port_names = [ p.name for p in component.analog_ports if p.mode=='recv']
#        self.send_analog_port_names = [ p.name for p in component.analog_ports if p.mode=='send']






class ComponentValidatorEventPorts(ComponentValidatorPerNamespace):
    """Check that each InputEvent and OutputEvent has a corresponding EventPort defined,
    and that the EventPort has the right direction. 
    """
    
    def __init__(self, component):
        ComponentValidatorPerNamespace.__init__(self, explicitly_require_action_overrides=False)
        
        
        #Mapping component to list of events/eventports at that component
        self.events_ports = defaultdict( dict )
        self.output_events = defaultdict( list )
        self.input_events = defaultdict( list )
        
        self.visit(component)
        
        # Check that each output event has a corresponding event_port with a send mode: 
        for ns, output_events in self.output_events.iteritems():
            for output_event in output_events:
                
                assert output_event in self.events_ports[ns], "Can't find port definition matching OP-Event: %s"%output_event
                assert self.events_ports[ns][output_event].mode == 'send'
        
        # Check that each input event has a corresponding event_port with a recv/reduce mode: 
        for ns, input_events in self.input_events.iteritems():
            for input_event in input_events:
                assert input_event in self.events_ports[ns]
                assert self.events_ports[ns][input_event].mode in ('recv','reduce')
        
        
        #Check that each Event port emits/recieves at least one
        for ns, event_ports in self.events_ports.iteritems():
            for evt_port_name in event_ports.keys():
                
                op_evts_on_port = [ ev for ev in self.output_events[ns] if ev==evt_port_name]
                ip_evts_on_port = [ ev for ev in self.input_events[ns]  if ev==evt_port_name]
                
                if len(op_evts_on_port) + len(ip_evts_on_port) == 0:
                    print 'Unable to find events generated for: ', ns, evt_port_name
                    assert False
            
        
    def action_eventport(self, port, namespace, **kwargs):
        assert not port.name in self.events_ports[namespace]
        self.events_ports[namespace][port.name] = port
        
    def action_outputevent(self, output_event, namespace, **kwargs):
        self.output_events[namespace].append( output_event.port_name)
                
    def action_onevent(self, on_event, namespace, **kwargs):
        self.input_events[namespace].append( on_event.src_port_name)
        
        
        



    
    
        
        
        
        
# Check that the sub-components stored are all of the
# right types:
class ComponentValidatorOutputAnalogPorts(ComponentValidatorPerNamespace):
    """ Check that all output AnalogPorts reference a local symbol, either an alias or a state variable 
    """
     
    def __init__(self, component):
        ComponentValidatorPerNamespace.__init__(self, explicitly_require_action_overrides=False)
        
        self.output_analogports = defaultdict(list)
        self.available_symbols = defaultdict(list)
        
        self.visit(component)
        
        for namespace, analogports in self.output_analogports.iteritems():
            for ap in analogports:
                assert ap in self.available_symbols[namespace]
    
    
    def add_symbol(self, namespace, symbol):
        assert not symbol in self.available_symbols[namespace] 
        self.available_symbols[namespace].append(symbol)
    
    def action_analogport(self, port, namespace, **kwargs):
        if not port.is_incoming():
            self.output_analogports[namespace].append(port.name)
            
    def action_statevariable(self, state_variable, namespace, **kwargs):
        self.add_symbol(namespace=namespace, symbol=state_variable.name)
                        
    def action_alias(self, alias, namespace, **kwargs):
        self.add_symbol(namespace=namespace, symbol=alias.lhs)
        


            
        

