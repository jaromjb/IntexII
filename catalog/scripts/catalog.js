$((function(context){

    return function(){

        $.ajax({
            "url": "/catalog/api.getdata/"
        }).done(function(data) {
            console.log("IT'S BACK");
            console.log(data);
        });

    }

})(DMP_CONTEXT.get()));
 