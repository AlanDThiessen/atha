
// Use Jquery to start the app when the DOM is ready
//$(document).ready( main );

function LightChange( lightId )
{
   $.ajax(
   {
      url: 'setLight',
      data: 
      type: 'GET',
      //error : function () { document.title='error'; }, 
      success: function (data)
      {
         $('#ajax_content').html(data);
      }
   } );
}