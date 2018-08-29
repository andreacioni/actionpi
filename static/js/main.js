setInterval(reload_cpu_load, 2000)


function is_recording() {

}

function stop_recording() {
    $.get('api/start').done(
        function() {

        }
    )
}

function start_recording() {
    $.get('api/stop').done(
        function() {
            
        }
    ).fail(
        function() {

        }
    )
}