window.addEventListener('load',createEvent_use_tame_range)
window.addEventListener('load', get_changes_default)

function createEvent_use_tame_range(){

    var use_time_range = document.getElementById('id_use_time_range')
    use_time_range.addEventListener("change", change_trigger)

}

function get_changes_default(e) {
    var use_time_range = document.getElementById('id_use_time_range')
    change_availability_time_range_inputs(use_time_range.checked)
}

function change_trigger(e) {
    change_availability_time_range_inputs(e.target.checked)
}

function change_availability_time_range_inputs(availability) {
    var input_list = document.getElementsByClassName('range-time-input')
    for (let i = 0; i < input_list.length; i++) {
        input_list[i].readOnly = !availability
    }
}