:- dynamic parent/2.
:- dynamic slot/4.
:- dynamic object_instance/2.

parent(device, smart_entity).
parent(user, smart_entity).
parent(automation_scenario, smart_entity).
parent(sensor, device).
parent(actuator, device).
parent(temperature_sensor, sensor).
parent(light_sensor, sensor).
parent(heater, actuator).
parent(smart_light, actuator).
parent(admin_user, user).
parent(regular_user, user).
parent(smart_entity, null).

slot(smart_entity, name, 'UnnamedEntity', none).
slot(smart_entity, status, 'inactive', none).

slot(device, location, 'unknown_location', none).

slot(sensor, last_reading, 0, if_needed(request_sensor_data)).
slot(sensor, unit, 'N/A', none).

slot(temperature_sensor, unit, 'Celsius', none).
slot(temperature_sensor, threshold, 25, none).

slot(light_sensor, unit, 'Lux', none).

slot(actuator, power_level, 0, none).
slot(actuator, is_on, no, if_changed(actuator_switched)).

slot(heater, max_temp, 30, none).

slot(smart_light, brightness, 50, if_changed(light_brightness_changed)).

slot(user, username, 'unknown_user', none).
slot(admin_user, privileges, 'full_access', none).
slot(regular_user, privileges, 'limited_access', none).

slot(automation_scenario, condition, 'no_condition', none).
slot(automation_scenario, action, 'no_action', if_added(log_new_scenario)).

request_sensor_data(ClassOrObj, SlotName, Value) :-
    format("Slot ~w for ~w is not defined. Please enter a new sensor value: ", [SlotName, ClassOrObj]),
    read(UserInput),
    retractall(slot(ClassOrObj, SlotName, _, _)),
    asserta(slot(ClassOrObj, SlotName, UserInput, none)),
    Value = UserInput.

actuator_switched(ClassOrObj, SlotName, NewValue) :-
    format("Device ~w: slot ~w changed to ~w. ", [ClassOrObj, SlotName, NewValue]),
    ( NewValue = yes ->
        format("Now the device is turned on.~n", [])
    ; NewValue = no ->
        format("Now the device is turned off.~n", [])
    ; format("Unknown state: ~w~n", [NewValue])
    ).

light_brightness_changed(ClassOrObj, SlotName, NewVal) :-
    format("Light ~w: brightness changed to ~w.~n", [ClassOrObj, NewVal]),
    ( NewVal =:= 0 ->
        format("Brightness 0 => turning the light off.~n", []),
        set_slot(ClassOrObj, is_on, no)
    ; NewVal > 0 ->
        set_slot(ClassOrObj, is_on, yes)
    ; true
    ).

log_new_scenario(ClassOrObj, SlotName, ActionValue) :-
    format("A scenario ~w was added with an action: ~w~n", [ClassOrObj, ActionValue]).

get_slot(ClassOrObj, SlotName, Value) :-
    slot(ClassOrObj, SlotName, StoredValue, ProcType),
    !,
    ( ProcType = if_needed(Goal),
      (StoredValue = 'N/A' ; StoredValue = 'unknown' ; StoredValue = 0) ->
        call(Goal, ClassOrObj, SlotName, DynamicValue),
        Value = DynamicValue
    ; ProcType = if_needed(Goal),
      StoredValue = SomeVal,
      SomeVal \= 'N/A' ->
        Value = SomeVal
    ; otherwise ->
        Value = StoredValue
    ).

get_slot(ClassOrObj, SlotName, Value) :-
    parent(ClassOrObj, Parent),
    Parent \= null,
    !,
    get_slot(Parent, SlotName, Value).

get_slot(_, SlotName, not_found) :-
    format("Slot ~w not found in the hierarchy.~n", [SlotName]),
    fail.

set_slot(ClassOrObj, SlotName, NewValue) :-
    ( slot(ClassOrObj, SlotName, OldValue, ProcType) ->
        retractall(slot(ClassOrObj, SlotName, _, _)),
        asserta(slot(ClassOrObj, SlotName, NewValue, ProcType)),
        ( ProcType = if_changed(Goal) ->
            call(Goal, ClassOrObj, SlotName, NewValue)
        ; true
        ),
        format("Slot ~w of ~w changed. Old: ~w, new: ~w.~n",
               [SlotName, ClassOrObj, OldValue, NewValue])
    ; asserta(slot(ClassOrObj, SlotName, NewValue, none)),
      format("A new slot ~w was added to ~w. Value: ~w.~n",
             [SlotName, ClassOrObj, NewValue]),
      ( slot(ClassOrObj, SlotName, NewValue, if_added(Goal)) ->
            call(Goal, ClassOrObj, SlotName, NewValue)
      ; true
      )
    ).

create_object(ObjName, ClassName) :-
    asserta(object_instance(ObjName, ClassName)),
    format("Created object ~w of class ~w.~n", [ObjName, ClassName]).

get_value_for_object(ObjName, SlotName, Value) :-
    ( slot(ObjName, SlotName, StoredValue, ProcType) ->
        ( ProcType = if_needed(Goal),
          StoredValue = 'N/A' ->
            call(Goal, ObjName, SlotName, DynamicValue),
            Value = DynamicValue
        ; Value = StoredValue
        )
    ; object_instance(ObjName, ClassName),
      get_slot(ClassName, SlotName, Value)
    ).

set_value_for_object(ObjName, SlotName, NewValue) :-
    slot(ObjName, SlotName, OldVal, ProcType),
    !,
    retractall(slot(ObjName, SlotName, _, _)),
    asserta(slot(ObjName, SlotName, NewValue, ProcType)),
    ( ProcType = if_changed(Goal) ->
        call(Goal, ObjName, SlotName, NewValue)
    ; true
    ),
    format("Slot ~w of object ~w changed from ~w to ~w.~n",
           [SlotName, ObjName, OldVal, NewValue]).

set_value_for_object(ObjName, SlotName, NewValue) :-
    asserta(slot(ObjName, SlotName, NewValue, none)),
    format("A new slot ~w was added to object ~w with value ~w.~n",
           [SlotName, ObjName, NewValue]).

% ?- [smart_home_frames].
% true.

% ?- create_object(myHeater, heater).
% Создан объект myHeater класса heater.
% true.

% ?- set_slot(myHeater, name, 'Living Room Heater').
% Добавлен новый слот name у myHeater. Значение: Living Room Heater.
% true.

% ?- set_slot(myHeater, is_on, yes).
% Устройство myHeater: значение is_on изменено на yes. Теперь устройство включено.
% Изменён слот is_on у myHeater. Старое: no, новое: yes
% true.

% ?- get_slot(myHeater, is_on, State).
% State = yes.

% ?- set_slot(myHeater, max_temp, 35).
% Добавлен новый слот max_temp у myHeater. Значение: 35.
% true.

% ?- create_object(myScenario, automation_scenario).
% Создан объект myScenario класса automation_scenario.
% true.

% ?- set_slot(myScenario, condition, 'temp<20').
% Добавлен новый слот condition у myScenario. Значение: temp<20.
% true.

% ?- set_slot(myScenario, action, 'turn on heater').
% Добавлен новый слот action у myScenario. Значение: turn on heater.
% Добавлен сценарий myScenario с действием: turn on heater
% true.

% ?- get_slot(myScenario, action, A).
% A = 'turn on heater'.

% ?- create_object(mary, regular_user).
% Создан объект mary класса regular_user.
% true.

% ?- set_slot(mary, username, 'mary_usr').
% Добавлен новый слот username у mary. Значение: mary_usr.
% true.

% ?- get_slot(mary, username, U).
% U = 'mary_usr'.
