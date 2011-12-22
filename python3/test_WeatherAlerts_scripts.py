'''
This file is to run nose tests on the scripts included with the module
'''


def test_nagios_plugin():
    from NagiosWeatherAlerts import loadalerts
    samecodes = '''016027,016001'''
    loadalerts(samecodes)