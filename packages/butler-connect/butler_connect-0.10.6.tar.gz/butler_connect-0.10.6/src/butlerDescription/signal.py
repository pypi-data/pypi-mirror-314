   
from marshmallow import Schema, fields,post_load
from datetime import datetime

class SignalType():
    unDef = 'undef'
    temperature = 'temperature'
    setTemperature = 'set_temperature'
    class setTemperature_():
        heater = 'set_temperature_heater'
        class heater_():
            comfort = 'set_temperature_heater_comfort'
            setback = 'set_temperature_heater_setback'
        cooler = 'set_temperature_cooler'
    humidity = 'humidity'
    windowIsOpen = 'window_is_open'
    presence = 'presence'
    motion = 'motion'
    presence_merged = 'presence_merged'
    illumination = 'illumination'
    co2 = 'co2'
    actuatorValue = 'actuator_value'
    systemState = 'system_state'
    vdd = 'vdd'
    battery = 'battery'
    class systemState_():
        heater = 'system_state_heater'
        heaterMode = 'system_state_heater_mode'
        tapWater = 'system_state_tap_water'
        tapWaterMode = 'system_state_tap_water_mode'
        cooler = 'system_state_cooler'
    consumptionGas = 'consumption_gas'
    consumptionGasRel = 'consumption_gas_rel'
    consumptionGasCurrent = 'consumption_gas_current'
    consumptionPower = 'consumption_power'
    consumptionPowerRel = 'consumption_power_rel'
    consumptionPowerCurrent = 'consumption_power_current'
    consumptionWater = 'consumption_water'
    consumptionWaterRel = 'consumption_water_rel'
    consumptionWaterCurrent = 'consumption_water_current'
    consumptionHeat = 'consumption_heat'
    consumptionHeatRel = 'consumption_heat_rel'
    consumptionHeatCurrent = 'consumption_heat_current'
    consumptionCool = 'consumption_cool'
    consumptionCoolRel = 'consumption_cool_rel'
    consumptionCoolCurrent = 'consumption_cool_current'
    class curve_():
        outsideTemperature = 'curve_outside_temperature'
        flowTemperature = 'curve_flow_temperature'
        flowTemperatureEco = 'curve_flow_temperature_eco'
        returnFlowTemperature = 'curve_return_flow_temperature'
    outsideTemperature = 'outside_temperature'    
    flowTemperature = 'flow_temperature'
    returnFlowTemperature = 'return_flow_temperature'
    storageTemperature = 'storage_temperature'
    freezProtectionTemperature = 'freez_protection_temperature'
    

class SignalOptionType():
    unDef = 'undef'
    forwardingMQTT = 'forwarding_mqtt'
    convertFrom    = 'convert_from'
    class buildingHardware():
        unDef = 'undef'
        heating = 'building_hardware_heating'
        heating_sub_system = 'building_hardware_heating_sub_system'
        cooling = 'building_hardware_cooling'
        ventilation = 'building_hardware_ventilation'
        lighting = 'building_hardware_lighting'
        energy = 'building_hardware_energy'
    
class SignalDirection():
    input = 'input'
    output = 'output'

def singnalDirection2Flags(direction):
    isInput = False
    isOutput = False
    if direction == SignalDirection.input:
        isInput = True
    elif direction == SignalDirection.output:
        isOutput = True
    return isInput,isOutput
    
class Signal():
    def __init__(self,type,component=0,group=0,ioDevice="",ioSignal="",parameter={},timestamp=datetime.now(),value = 0.0,valueStr = "",ext={}):
        self.timestamp  = timestamp
        self.component  = int(component)
        self.group      = int(group)
        self.ioDevice   = ioDevice
        self.ioSignal   = ioSignal
        self.type       = type
        self.value      = float(value)
        self.valueStr   = str(valueStr)
        self.ext        = dict(ext)
        
    def __repr__(self):
        return "<User(name={self.name!r})>".format(self=self)
    def __str__(self) -> str:
        return f'component={self.component}, group={self.group}, ioDevice={self.ioDevice}, ioSignal={self.ioSignal}, type={self.type}, value={self.value}, valueStr={self.valueStr}, timestmap={self.timestamp}, ext={self.ext}'        

class SignalSchmea(Schema):
    timestamp   = fields.DateTime(required=True)
    component   = fields.Int()
    group       = fields.Int()
    ioDevice    = fields.Str()
    ioSignal    = fields.Str()
    type        = fields.Str()
    value       = fields.Float()
    valueStr    = fields.Str()
    ext         = fields.Dict()
    
    @post_load
    def make_control(self, data, **kwargs):
        return Signal(**data)