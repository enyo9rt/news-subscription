const subscription = () => {
    let subscription_type = $("#subscription_type").val();
    let delivery_time = $("#delivery_time").val();
    let user_email = $('#user_email').val();

    $.ajax({
        type: 'POST',
        url: '/subscription',
        data: {
            subscription_type_give: subscription_type,
            delivery_time_give: delivery_time,
            user_email_give: user_email
        },
        success: function (response) {
            alert(response['msg'])
            window.location.reload()
        }
    });
}