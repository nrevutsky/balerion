/**
 * Created by python on 08.02.17.
 */

document.getElementById("show_about_text").onclick = function(){
    var is_about_text_shown = document.getElementById("about_text");
    if(is_about_text_shown.style.display == "" || is_about_text_shown.style.display == "none"){
        is_about_text_shown.style.display = "block";
    } else {
        is_about_text_shown.style.display = "none";
    }
};

document.getElementById("compute_button").onclick = function(){
    document.getElementById("waiting_text").style.display = "block";
};