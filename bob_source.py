import math

import obspython as obs


source_name = ''
running = False
counter = 0.0

def update_position():
    global source_name
    global counter
    source = obs.obs_frontend_get_current_scene()
    if source is not None:
        scene_object = obs.obs_scene_from_source(source)
        scene_item = obs.obs_scene_find_source(scene_object, source_name)
        pos = obs.vec2()
        obs.obs_sceneitem_get_pos(scene_item, pos)
        next_pos = obs.vec2()
        next_pos.x = pos.x
        y_adjust = math.sin(math.radians(counter))
        next_pos.y = pos.y + y_adjust / 4
        counter += 0.5
        if counter == 360:
            counter = 0
        obs.obs_sceneitem_set_pos(scene_item, next_pos)
        obs.obs_source_release(source)

def bob_pressed(props, prop):
    global running
    running = not running

def script_description():
    return 'Make a source bob up and down a bit.'

def script_tick(seconds):
    if running:
        update_position()

def script_update(settings):
    global source_name
    source_name = obs.obs_data_get_string(settings, "source")

def script_properties():
    props = obs.obs_properties_create()

    p = obs.obs_properties_add_list(props, "source", "Text Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_unversioned_id(source)
            name = obs.obs_source_get_name(source)
            obs.obs_property_list_add_string(p, name, name)

        obs.source_list_release(sources)

    obs.obs_properties_add_button(props, "button", "Bob", bob_pressed)
    return props
