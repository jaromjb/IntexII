(function(context) {
    return function(){

        var containers = $('.product-container');
        containers.each(function(i, container){
            var pid = $(container).attr('data-product-id');
            $.ajax({
                url: "/catalog/product.tile/" + pid,
            }).done(function(content){
                $(container).html(content);

            });
        })
    }
    
})(DMP_CONTEXT.get());
