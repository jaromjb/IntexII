// $((function(context) {
//     return function() {
//     var containers = $('.product-container');
//     containers.each(function(i,container){
//         console.log(container);
//         var pid = $(container).attr('data-product-id')
//         $.ajax({
//             "url": "/catalog/product.tile/"+ pid + "/",
//         }).done(function(data) {
//             $(container).html(data)
//         });
//     });  
// }
// })(DMP_CONTEXT.get()));