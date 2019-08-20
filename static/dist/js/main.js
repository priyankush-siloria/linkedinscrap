$(".status").click(function(){
	var status_value = $(this).val();
	var id_value = $(this).data("id");
  $.ajax({
  	url: "/status",
  	type: "POST",
  	data:{
  		"status":status_value,
  		"id":id_value,
  		"csrfmiddlewaretoken":token
  	},
  	success: function(result){
       $.toast({
            heading: 'Success',
            text: result.msg,
            icon: 'success',
            position :"top-center",
            loader:false,
            hideAfter:1000
        })
    	// alert(result.msg);
 	}});
});

$('#actionForm').on('submit', function() {
  // event.preventDefault();
  $('input[name="ids"]').val(ids);
   $('input[name="csrfmiddlewaretoken"]').val(token);

  // $.ajax({
  //   url: "/actions",
  //   type: "POST",
  //   data:{
  //     "action":action,
  //     "ids":allids,
  //     "csrfmiddlewaretoken":token
  //   },

  //   success: function(result){
  //      $.toast({
  //           heading: 'Success',
  //           text: result.msg,
  //           icon: 'success',
  //           position :"top-center",
  //           loader:false,
  //           hideAfter:1000
  //       })
  //     // alert(result.msg);
  // }});
});

$('.changestatus').on('click', function(){

  var status_value = $(this).val();
  console.log(status_value);

 $.ajax({
    url: "/changestatus",
    type: "POST",
    data:{
      "status":status_value,
      "csrfmiddlewaretoken":token
    },
    success: function(result){
       $.toast({
            heading: 'Success',
            text: result.msg,
            icon: 'success',
            position :"top-center",
            loader:false,
            hideAfter:1000
        })
      // alert(result.msg);
  }});
});

// Delete automation
  $('.delete').click(function(){
  var id=$(this).attr("data-id");
  $.ajax({
            url: "/delete-automation",
            type:"GET",
            data: {
               'id':id,
            },
            success: function(response) {
          
                if(response.status==true){
                  window.location.reload();
                }
                else
                {
                	$.toast({
                      heading: 'Error',
                      text: "Some error occured",
                      icon: 'error',
                      position :"top-center",
                      loader:false,
                      hideAfter:1000
                  })
                }
            }
        });
});

$('.approve').click(function()
{
  var id = $(this).attr('id');
  alert(id);
  console.log(id); 
  $.ajax({
    url: '/status',
    method: 'GET', // or another (GET), whatever you need
    data: {'id':id},
    success: function(data) 
    {
    //   if(response.status==true)
    //   {
    //   // window.location.reload();
    // }
  }

  });

});


//Delete User 
 $('.deleteuser').click(function(){
  var id=$(this).attr("data-id");
  $.ajax({
            url: "/delete-user",
            type:"GET",
            data: {
               'id':id,
            },
            success: function(response) {
          
                if(response.status==true){
                  window.location.reload();
                }
                else
                {
                  $.toast({
                      heading: 'Error',
                      text: "Some error occured",
                      icon: 'error',
                      position :"top-center",
                      loader:false,
                      hideAfter:1000
                  })
                }
            }
        });
});



$('.play').click(function()
{
  var id = $(this).attr('id');
  var linkedin_user=$(this).closest('td').next("input.linkedin-user").val();
  console.log(linkedin_user);
   // alert("Scraping is start it will be running at back-end.In case of error or scraped all data you will get the email on 'mario@sdg360.com' g-mail.");
   // alert("Script will automattally start and run at background. All alert will be send to mail. Final result can be seen on all data page.");
  $.ajax({
    url: '/thread',
    method: 'GET', // or another (GET), whatever you need
    data: {'id':id,'linkedin_user':linkedin_user},
    success: function(data) 
    {
      if(data.status==true)
      {
       $.toast({
              heading: 'Success',
              text: data.message,
              icon: 'success',
              position :"top-center",
              loader:false,
              hideAfter:3000
          })
     }
     else{
      $.toast({
              heading: 'Error',
              text: data.message,
              icon: 'error',
              position :"top-center",
              loader:false,
              hideAfter:5000
          })
     }
  }

  });

});

$('.pause').click(function()
{
  var id = $(this).attr('id');

  console.log(id); 
  $.ajax({
    url: '/stop',
    method: 'GET', // or another (GET), whatever you need
    data: {'id':id},
    success: function(data) 
    {
    //   if(response.status==true)
    //   {
    //   // window.location.reload();
    // }
  }

  });

});
