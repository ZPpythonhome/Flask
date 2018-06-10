$(function(){

    $("#all_type").click(function(){

        console.log("全部类型");

        $("#all_type_container").show();

        $(this).find("span").find("span").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");

             // $(this).slideUp();
        $("#sort_rule_container").hide();

        $("#sort_rule").find("span").find("span").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");

    })

    $("#all_type_container").click(function(){

        $(this).hide();

        $("#all_type").find("span").find("span").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");


    })

    $("#sort_rule").click(function(){
        console.log("排序规则");

        $("#sort_rule_container").show();

        $(this).find("span").find("span").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");

        $("#all_type_container").hide();

        $("#all_type").find("span").find("span").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");

    })

    $("#sort_rule_container").click(function () {

        // $(this).slideUp();
        $(this).hide();

        $("#sort_rule").find("span").find("span").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");

    })

    $(".addShopping").click(function(){
    //    获取属性   提供两种方式   attr    prop
    //    attr  可以获取任意属性，不管属性是怎么来的
    //    prop  只能获取内置属性
            var $addShopping = $(this);

            // console.log($addShopping.prop('goodsid'));
            //
            // console.log($addShopping.attr('goodsid'));
            var goodsid = $addShopping.attr('goodsid');

            console.log(goodsid);

            $.getJSON('/axf/addtocart/', {'goodsid': goodsid}, function (data) {
                console.log(data);

                if (data['status'] == '200'){
                    var goods_num = data['goods_num'];
                    $addShopping.prev().html(goods_num);

                }else if(data['status'] == '302'){
                    window.open('/axf/userlogin/', target='_self');
                }

            })

    })


    $(".subShopping").click(function () {

    })

})