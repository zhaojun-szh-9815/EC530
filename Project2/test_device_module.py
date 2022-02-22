import pytest
import device_module as dev

@pytest.mark.parametrize('type, value_type, output',
                         [('height_machine', 'Height',
                           "[{'d_id': 1, 'type': 'sphygmomanometer', 'value_type': 'Blood_Pressure'}, {'d_id': 2, 'type': 'thermometer', 'value_type': 'Temperature'}, {'d_id': 3, 'type': 'pulse_device', 'value_type': 'Pulse'}, {'d_id': 4, 'type': 'oximeter', 'value_type': 'Blood_Oxygen'}, {'d_id': 5, 'type': 'weight_machine', 'value_type': 'Weight'}, {'d_id': 6, 'type': 'glucometer', 'value_type': 'Blood_Glucose'}, {'d_id': 7, 'type': 'height_machine', 'value_type': 'Height'}]")])
def test_devices_registration(type, value_type, output):
    dev.make_json_input()
    devices = dev.device_registration(type, value_type)
    assert str(devices) == output


@pytest.mark.parametrize('assign_person, assigned_to, device, output',
                         [(2, 3, 3,"[{'a_id': 1, 'assign_person': 2, 'assigned_to': 3, 'device': 1}, {'a_id': 2, 'assign_person': 2, 'assigned_to': 3, 'device': 2}, {'a_id': 3, 'assign_person': 2, 'assigned_to': 3, 'device': 3}]" ),
                          (3, 3, 3, "[{'a_id': 1, 'assign_person': 2, 'assigned_to': 3, 'device': 1}, {'a_id': 2, 'assign_person': 2, 'assigned_to': 3, 'device': 2}]"),
                          (2, 2, 3, "[{'a_id': 1, 'assign_person': 2, 'assigned_to': 3, 'device': 1}, {'a_id': 2, 'assign_person': 2, 'assigned_to': 3, 'device': 2}]"),
                          (2, 3, 8, "[{'a_id': 1, 'assign_person': 2, 'assigned_to': 3, 'device': 1}, {'a_id': 2, 'assign_person': 2, 'assigned_to': 3, 'device': 2}]")])
def test_new_assignment(assign_person, assigned_to, device, output):
    dev.make_json_input()
    assignments = dev.new_assignment(assign_person, assigned_to, device)
    assert str(assignments) == output

@pytest.mark.parametrize('assignment, value, output',
                         [(1, 110, "[{'r_id': 1, 'a_id': 1, 'value': 100.0}, {'r_id': 2, 'a_id': 2, 'value': 37.5}, {'r_id': 3, 'a_id': 1, 'value': 110}]"),
                          (3, 100, "[{'r_id': 1, 'a_id': 1, 'value': 100.0}, {'r_id': 2, 'a_id': 2, 'value': 37.5}]")]
                         )
def test_new_data_capture(assignment, value, output):
    dev.make_json_input()
    records = dev.new_data_captured(assignment, value)
    assert str(records) == output