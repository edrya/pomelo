$(document).ready(function () {

    $("#getStatusForm").submit(function (event) {
        event.preventDefault();

        /* get the action attribute from the <form action=""> element */
        var $form = $(this), url = $form.attr('action');
        var tasks = $(".task");

        var status_data_list = tasks.map(function () {
            return $(this).data("status");
        }).get();

        var task_id_data_list = tasks.map(function () {
            return $(this).data("task-id");
        }).get();

        var counter = 0;

        var number_of_tasks = tasks.length;


        // todo: replace with Socket.IO
        // Put tasks into queue
        function dispatch_work() {
            $.ajax({
                type: "post",
                url: "/dispatch",
                data: {
                    status: status_data_list,
                    ids: task_id_data_list
                },
                success: function (data) {
                    $('.bar').show();
                    $('.load-bar').show();
                    getting_status();

                }
            });
        }

        dispatch_work();

        // Need to poll the server to get updated statuses
        function getting_status() {
            $.ajax({
                type: "post",
                url: url,
                data: {
                    status: status_data_list,
                    ids: task_id_data_list
                },
                success: function (data) {
                    counter = 0;
                    $.each(data, function (k, v) {
                        // console.log(k, v['status']);
                        if (v['status'] === 'completed') {
                            counter++;
                            updating_status(v)
                        }
                    });

                    if (counter !== number_of_tasks) {
                        setTimeout(function () {
                            getting_status()
                        }, 5000);
                    }
                    else {

                        $('.bar').hide();
                        $('.load-bar').hide();
                    }
                }
            });
        }

    });

    function updating_status(completed) {
        var task_id = completed['id'];
        var status = completed['status'];
        var value = completed['value'];

        var first = $('tr[data-task-id="' + task_id + '"]').find('td:nth-child(1) i');
        var second = $('tr[data-task-id="' + task_id + '"]').find('td:nth-child(2) i');
        var third = $('tr[data-task-id="' + task_id + '"]').find('td:nth-child(3) i');

        second.addClass('success-text').html(status);
        third.html(completed['value']);


    }

});
