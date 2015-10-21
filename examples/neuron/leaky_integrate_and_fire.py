from nineml import abstraction as al, user as ul
from nineml import units as un
from nineml.xmlns import etree, E


def create_leaky_integrate_and_fire():
    dyn = al.Dynamics(
        name='LeakyIAF',
        regimes=[
            al.Regime('dv/dt = (i_synaptic*R - v)/tau',
                      transitions=[al.On('v > v_threshold',
                                         do=[al.OutputEvent('output_spike'),
                                             al.StateAssignment(
                                                 'end_refractory',
                                                 't + refractory_period'),
                                             al.StateAssignment('v',
                                                                'v_reset')],
                                         to='refractory')],
                      name='subthreshold'),
            al.Regime(transitions=[al.On('t > end_refractory',
                                   to='subthreshold')],
                      name='refractory')],
        state_variables=[al.StateVariable('v', dimension=un.voltage),
                         al.StateVariable('end_refractory',
                                          dimension=un.time)],
        parameters=[al.Parameter('R', un.resistance),
                    al.Parameter('refractory_period', un.time),
                    al.Parameter('v_reset', un.voltage),
                    al.Parameter('v_threshold', un.voltage),
                    al.Parameter('tau', un.time)],
        analog_ports=[al.AnalogReducePort('i_synaptic', un.current,
                                          operator='+')])

    return dyn


def parameterise_leaky_integrate_and_fire():

    comp = ul.DynamicsComponent(
        name='SampleLeakyIAF',
        definition=create_leaky_integrate_and_fire(),
        properties=[ul.Property('tau', 20.0, un.ms),
                    ul.Property('v_threshold', 20.0, un.mV),
                    ul.Property('refractory_period', 2.0, un.ms),
                    ul.Property('v_reset', 10.0, un.mV),
                    ul.Property('R', 1.5, un.Mohm)],
        initial_values=[ul.Initial('V', -70, un.mV)])
    return comp


if __name__ == '__main__':
    print etree.tostring(
        E.NineML(
            create_leaky_integrate_and_fire().to_xml(),
            parameterise_leaky_integrate_and_fire().to_xml()),
        encoding="UTF-8", pretty_print=True, xml_declaration=True)
