
// Use Jquery to start the app when the DOM is ready
$(document).ready( main );

function GetLights()
{
   $.ajax( {
      url:  "localhost:8080/getLights",
      //data: {},
      success: function( data )
      {
         var cntr;
         var xml = $.parseXML( data );

         console.log( data );
         if( $(xml).children( 'lights' ).length )
         {
            elemArray = $(xml).children( 'lights' ).children( 'light' );

            for( cntr = 0; cntr < elemArray.length; cntr++ )
            {
               var name       = $(elemArray[cntr]).attr( 'name' );
               var dimmable   = false;
               
               if( $(elemArray[cntr]).attr( 'dimmable' ) == 'yes' )
               {
                  dimmable = true;
               }
               
               DisplayLight( name, dimmable );
            }
         }
         
         //$( "#weather-temp" ).html( "<strong>" + data + "</strong> degrees" );
      } } );
}


function DisplayLight( name, dimmable )
{
   data  = "<label for='flip-1'>" + name + "</label>\n";
   data += "   <select name='flip-1' id='flip-1' data-role='slider'>\n";
   data += "      <option value='off'>Off</option>\n";
   data += "      <option value='on'>On</option>\n";
   data += "   </select>\n";

   if( dimmable == true )
   {
      data += "   <label for='slider-10'>Level:</label>\n";
      data += "   <input name='slider-10' id='slider-10' data-highlight='true' value='100' min='0' max='100' step='4' type='range'>\n";
   }
}