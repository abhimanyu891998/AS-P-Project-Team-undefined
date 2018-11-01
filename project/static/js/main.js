$(function(){

    let obj = {}, weight = 0.0;

    $(".plus").on("click", function(){
        if(obj[$(this).data("id")]) obj[$(this).data("id")]+=1
        else obj[$(this).data("id")]=1
        $(this).prev()[0].innerHTML = obj[$(this).data("id")];
        weight += parseFloat($(this).data("wt"))
    });
    $(".minus").on("click", function(){
        var x = obj[$(this).data("id")];
        if(x){
            obj[$(this).data("id")]-=1
            $(this).next()[0].innerHTML = obj[$(this).data("id")];
            if (x==1) delete obj[$(this).data("id")]
        }
        weight -= parseFloat($(this).data("wt"))


    });
    $(".value").on("click", function(){
        console.log(obj);
        console.log(weight)
    });


    $(".arrow").on("click", function(){
      $(this).toggleClass("toggled");
      $(this).parent().next().slideToggle();
    })

    $(".addToCart").on("click", function(){

        if(weight<=25.0){
            let data = {obj:obj, totalWeight: weight};
            $.ajax({
              type: "POST",
              url: "http://localhost:8000/orders/supplies",
              data: JSON.stringify(data),
              success: function(){
                console.log("Yay!")
              },
            });
        }
        else{
            $(".errorMessage").show();
            setTimeout($(".errorMessage").hide(), 2000);
        }

    })

});