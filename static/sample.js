
function clearvalue() {
    document.getElementById("text").value = "";
    document.getElementById("file1").value="";
    document.getElementById("key").value = "";
    document.getElementById("pass").value="";
    console.log(document.getElementById("pass").value,document.getElementById("file1").value)
  }
  
  function showImage(src, target) {
    var fr = new FileReader();
  
     fr.onload = function(){
  target.src = fr.result;
  }
   fr.readAsDataURL(src.files[0]);
  
  }
  function putImage() {
    var src = document.getElementById("select_image");
    var target = document.getElementById("target");
    showImage(src, target);
  }
  
  
  
  function scrollToSection(sectionId) {
      var section = document.getElementById(sectionId);
      section.scrollIntoView({ behavior: 'smooth' });
    }
  
  
  function valid(){
    var key=document.getElementById('key');
    var pass=1234;
    if (key.value != pass){
      alert("Password is not valid");
    }
  }
  