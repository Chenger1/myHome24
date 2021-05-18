function setPreview(input){
  if(input.files && input.files[0]){ // check if input widget uploads any files
    let reader = new FileReader(); // create new instance of FileReader object

    reader.onload = function(e){ // set function to onload handler to set new image preview
      $(input).closest('div[class*=col]').find('.preview_img').attr('src', e.target.result);
      // fidn parent column div and search for closes image preview
    };

    reader.readAsDataURL(input.files[0]); 
    // read data as a base64 coded url. It needs to put src to image element
  };
};