
// Use Jquery to start the app when the DOM is ready
//$(document).ready( main );

$(function()
{
   $('body').append( "<div class='ui-loader-background'> </div>" );
} );


function ModalPleaseWait()
{
   $.mobile.loading( 'show',
   {
      text:  'Please wait...',
      textVisible: true,
      theme: 'a',
      textonly: false,
    } );
}


function HidePleaseWait()
{
   $.mobile.loading( 'hide' );
}


function LightChange( lightId )
{
   var lightSwitch = $('#'+lightId);
   var status = lightSwitch.val();

   ModalPleaseWait();
   
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
         HidePleaseWait();
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
   
   
   ModalPleaseWait();
   
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
         HidePleaseWait();
      }
   } );

   return false;
}