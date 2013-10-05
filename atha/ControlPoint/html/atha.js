
// Use Jquery to start the app when the DOM is ready
//$(document).ready( main );

function LightChange( lightId )
{
   var lightSwitch = $('#'+lightId);
   var status = lightSwitch.val();
   
   $.ajax(
   {
      url: 'setLights',
      data: { action: status,
              id:     lightId
            },  
      type: 'GET',
      //error : function () { document.title='error'; }, 
      success: function (data)
      {
         // do nothing
      }
   } );

   return false;
}


function SetBrightness( sliderId, lightId )
{
   var slider = $('#'+sliderId);
   console.log( slider );
   var status = slider.val();
   var oldValue = slider.before();
   
  
   $.ajax(
   {
      url: 'setLights',
      data: { action: 'level',
              id:     lightId,
              value:  status
            },  
      type: 'GET',
      //error : function () { document.title='error'; }, 
      success: function (data)
      {
         // do nothing
      }
   } );

   return false;
}