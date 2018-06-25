function data_security(){

    var $password = $("#u_password");

    $password.val(md5($password.val()));

    return true;
}