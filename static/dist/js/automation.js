// Delete automation
  $('.delete').click(function(){
  var id=$(this).attr("data-id");
  $.ajax({
            url: "delete-automation",
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
                  alert("Error");
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
                  alert("Error");
                }
            }
        });
});



$('.play').click(function()
{
  var id = $(this).attr('id');
  alert("Scraping is start it will be running at back-end.In case of error or scraped all data you will get email on 'mario@sdg360.com this g-mail. And you can see scraped data on this link:http://206.189.197.174:1701/alldata. Thanks");
  $.ajax({
    url: '/thread',
    method: 'GET', // or another (GET), whatever you need
    data: {'id':id},
     
    success: function(data) 
    {
     
    //   if(response.status==true)
    //   {
    //   // window.location.reload();
    // }
    alert("data scraped successfully.")
  }

  });

});

$('.pause').click(function()
{
  var id = $(this).attr('id');
  alert(id);
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


