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

            weight -= parseFloat($(this).data("wt"))
        }




    });
    $(".value").on("click", function(){
        console.log(obj);
        console.log(weight)
    });


    $(".arrow").on("click", function(){
      $(this).toggleClass("toggled");
      $(this).parent().next().slideToggle();
    })


    $(".option").on("click", function(){
        let category = $(this).data("category")
        $(".item").hide();
        $(".item."+category).show();
        $(".dropbtn")[0].innerHTML=category;
    })

    $(".addToCart").on("click", function(){

        if(weight<=25.0 && weight>0){
            let data = {obj:obj, totalWeight: weight};
//            console.log(JSON.stringify(data))
            $.ajax({
              type: "POST",
              url: "/orders/supplies",
              contentType: 'application/json',
              data: JSON.stringify(data),
              success: function(){
                console.log("Yay!")
              },
              error: function(e){
                console.log(e)
              }
            });
        }
        else{
            window.alert("Exceeded!")
            $(".errorMessage").show();
            setTimeout($(".errorMessage").hide(), 2000);
        }

    })


    $(".dropbtn").on("click", function(){
        $(this).toggleClass("openCategories");
        $("#myDropdown").toggleClass("show");
    });

    // Close the dropdown menu if the user clicks outside of it
    window.onclick = function(event) {
      if (!event.target.matches('.dropbtn')) {

        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
          var openDropdown = dropdowns[i];
          if (openDropdown.classList.contains('show')) {
            openDropdown.classList.remove('show');
          }
        }
      }
    }

});