$(function(){

    let obj = {}, weight = 0.0, priority=-1;

    $(".plus").on("click", function(){
        if(obj[$(this).data("id")]) obj[$(this).data("id")]+=1
        else obj[$(this).data("id")]=1
        $(this).prev()[0].innerHTML = obj[$(this).data("id")];
        weight += parseFloat($(this).data("wt"))
        $("#current-weight").text(weight.toFixed(4));
    });
    $(".minus").on("click", function(){
        var x = obj[$(this).data("id")];
        if(x){
            obj[$(this).data("id")]-=1
            $(this).next()[0].innerHTML = obj[$(this).data("id")];
            if (x==1) delete obj[$(this).data("id")]

            weight -= parseFloat($(this).data("wt"))
            $("#current-weight").text(weight.toFixed(4));
        }




    });
    $(".value").on("click", function(){
        console.log(obj);
        console.log(weight)
        console.log(priority)
    });


    $(".arrow").on("click", function(){
      $(this).toggleClass("toggled");
      $(this).parent().next().slideToggle();
    })

    $(".priority-item").on("click", function(){
        $(".priority-item").removeClass("active");
        $(this).addClass("active");
        priority = $(this).data("priority");
    });

    $(".option").on("click", function(){
        let category = $(this).data("category")
        $(".item").hide();
        $(".item."+category).show();
        $(".dropbtn.categories")[0].innerHTML=category;
    })

    $(".addToCart").on("click", function(){

        if(weight<=25.0 && weight>0){
            let data = {obj:obj, totalWeight: weight.toFixed(4), priority: priority};
            $.ajax({
              type: "POST",
              url: "/orders/supplies",
              contentType: 'application/json',
              data: JSON.stringify(data),
              success: function(){
                console.log("Yay!")
                window.alert("Your order has been successfully placed!");
                weight=0.0;
                $("#current-weight").text(weight.toFixed(4));
                $(".value").text(0)

                obj = {};
              },
              error: function(e){
                console.log(e)
              }
            });
        }
        else{

            let message = weight >0 ? "You have exceeded the maximum amount, please try again!" : "You haven't selected anything!";
            window.alert(message)


//            $(".errorMessage").show();
//            setTimeout($(".errorMessage").hide(), 2000);
        }

    })


    $(".dropbtn.categories").on("click", function(){
        $(this).toggleClass("openCategories");
        $("#dropdownCategories").toggleClass("show");
    });

    $(".dropbtn.navbar").on("click", function(){
        $(this).toggleClass("openCategories");
        $(".navbarDropdown").toggleClass("show");
    });

    $(".forgotPassword").on("click", function(){
        console.log("Clicked button :)");
        var username = prompt("Please enter your username:");
        $.ajax({
            type: "POST",
            url: "/forgot-password",
            contentType: 'application/json',
            data: JSON.stringify({username:username}),
            success: function(data){
                window.alert("Request sent!")
            },
            error: function(e){
              console.log(e)
              window.alert("Something went wrong!")
            }

        })
    })

    $(".sendPasswordResetLink").on("click", function(){
        var username = $(this).data("username")
        $.ajax({
            type: "POST",
            url: "/send-link",
            contentType: 'application/json',
            data: JSON.stringify({username:username}),
            success: function(data){
                window.alert("Link sent!")
            },
            error: function(e){
              console.log(e)
              window.alert("Something went wrong!")
            }

        })
    })

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


    $(".cancelOrder").on("click", function(){
        var id = $(this).data("id")
        var actionType = $(this).data("type")
        var action = {id: id, type: actionType}
        if(confirm("Are you sure you want to cancel this order?")){
            $.ajax({
                type: "POST",
                url: "/orders/myorders",
                contentType: 'application/json',
                data: JSON.stringify({actionType:actionType, id:id}),
                success: function(data){
                    location.reload();
                    window.alert("Successfully deleted!");
                },
                error: function(e){
                  console.log(e)
                  window.alert("Something went wrong!")
    
                }
    
            })
        }
        
  });

    $(".notifyDelivery").on("click", function(){
        var id = $(this).data("id")
        var actionType = $(this).data("type")
        var action = {id: id, type: actionType}
        $.ajax({
            type: "POST",
            url: "/orders/myorders",
            contentType: 'application/json',
            data: JSON.stringify({actionType:actionType, id:id}),
            success: function(data){
                $(".notifyDelivery-"+id).text("Delivered!")
                $(".notifyDelivery-"+id).addClass("notified")
                $(".notifyDelivery-"+id).attr("disabled", "disabled");
                window.alert("Success!")
                location.reload();
            },
            error: function(e){
              console.log(e)
              window.alert("Something went wrong!")

            }

    })
  });
  $(".updateUserDetails").on("click", function(e){
    e.preventDefault();
    window.alert("Success!")
    $("#updateUserDetailsForm").submit();
  })
});
