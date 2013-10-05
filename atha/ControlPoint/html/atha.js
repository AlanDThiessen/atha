
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

function SetBrightness( lightId )
{
}