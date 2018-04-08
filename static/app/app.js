$(document).ready(function(){
    $('.individual_post').click(function(){
        $('#' + $(this).attr('id') + '-modal').modal('show');
    });
});