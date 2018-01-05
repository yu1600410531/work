function DoSubmit() {
    var input_dict = {};
    $('input').each(function () {
        var v = $(this).val();
        var n = $(this).attr('name');
        input_dict[n] = v;
    });
    console.log(input_dict);
    $('.error-msg').remove();
    $.ajax({
        url:'/reg/',
        type:'POST',
        data:input_dict,
        dataType:'json',
        success:function (result) {
            if(result.status){
                location.href = '/index/'
            }else{
                $.each(result.message,function (k,v) {
                    console.log(k,v[0].message);
                    var tag = document.createElement('span');
                    tag.className = 'error-msg';
                    tag.innerText = v[0].message;
                    $('input[name="'+k+'"]').after(tag);
                })
            }

        },
        error:function () {

        },



    })
    
}