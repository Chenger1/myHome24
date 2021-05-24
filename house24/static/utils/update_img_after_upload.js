function setPreview(input, selector='div[class*=col]', image_selector='.preview_img'){
  if(input.files && input.files[0]){ // check if input widget uploads any files
    let reader = new FileReader(); // create new instance of FileReader object

    reader.onload = function(e){ // set function to onload handler to set new image preview
      $(input).closest(selector).find(image_selector).attr('src', e.target.result);
      // fidn parent column div and search for closes image preview
    };

    reader.readAsDataURL(input.files[0]); 
    // read data as a base64 coded url. It needs to put src to image element
  };
};