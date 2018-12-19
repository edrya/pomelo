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

        // Need to poll the server to get updated statuses
        // todo: replace with Socket.IO
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

                        }
                    });

                    if (counter !== number_of_tasks) {
                        console.log(counter);
                        setTimeout(function () {
                            send();
                        }, 500);
                    }
                }
            });
        }

        getting_status();

    });

});
