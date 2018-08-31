function reload_status() {
    $.get("api/status").done(
        function(data) {
            $("#cpu_temp").text(data.system.cpu_temperature)
            $("#cpu_load").text(data.system.cpu_load)
            $("#mem_use").text(data.system.mem_usage)
            $("#disk_use").text(data.system.disk_usage)

            $("#fps_label").text(data.framerate)
            $("#fps_range").val(data.framerate)

            if (data.recording === true) {
                $("#is_recording").text("Started")
                $("#start_btn").prop('disabled', true)
                $("#stop_btn").prop('disabled', false)
                $("#fps_range").prop('disabled', false)
            } else if (data.recording === false) {
                $("#is_recording").text("Stopped")
                $("#start_btn").prop('disabled', false)
                $("#stop_btn").prop('disabled', true)
                $("#fps_range").prop('disabled', true)
            } else {
                $("#is_recording").text("n.a.")
                $("#fps_range").text("n.a.")
                $("#start_btn").prop('disabled', true)
                $("#stop_btn").prop('disabled', true)
                $("#fps_range").prop('disabled', true)
            }
        }
    )
}

function stop_recording() {
    var previous_state_start = $("#start_btn").prop('disabled')
    var previous_state_stop = $("#stop_btn").prop('disabled')
    
    $.get("api/stop").done(
        function() {
            $("#start_btn").prop('disabled', false)
            $("#stop_btn").prop('disabled', true)
            $("#fps_range").prop('disabled', false)
        }
    ).fail(
        function() {
            $("#start_btn").prop('disabled', previous_state_start)
            $("#stop_btn").prop('disabled', previous_state_stop)
            $("#fps_range").prop('disabled', false)
        }
    )
}

function start_recording() {
    var previous_state_start = $("#start_btn").prop('disabled')
    var previous_state_stop = $("#stop_btn").prop('disabled')
    $.get("api/start").done(
        function() {
            $("#start_btn").prop('disabled', true)
            $("#stop_btn").prop('disabled', false)
            $("#fps_range").prop('disabled', true)
        }
    ).fail(
        function() {
            $("#start_btn").prop('disabled', previous_state_start)
            $("#stop_btn").prop('disabled', previous_state_stop)
            $("#fps_range").prop('disabled', false)
        }
    )


}

function change_fps(current_fps) {
    $.get("api/set?val=" + current_fps).done(
        function() {
            $("#fps_label").val(current_fps)
        }
    )
}

function halt() {
    $.get("api/halt").done(
        function() {
            $("#start_btn").prop('disabled', true)
            $("#stop_btn").prop('disabled', true)
            $("#fps_range").prop('disabled', true)
        }
    )
}

reload_status()

setInterval(reload_status, 2000)