$(document).ready(function() {

         $("#generate-string").click(function(e) {
           $.post("/generator", {"length": $("input[name=length]").val()})
            .done(function(string) {
               $("#the-string").show();
               $("#the-string input").val(string);
            });
           e.preventDefault();
         });

         $("#replace-string").click(function(e) {
           $.ajax({
              type: "PUT",
              url: "/generator",
              data: {"another_string": $("#the-string input").val()}
           })
           .done(function() {
              alert("Replaced!");
           });
           e.preventDefault();
         });

         $("#delete-string").click(function(e) {
           $.ajax({
              type: "DELETE",
              url: "/generator"
           })
           .done(function() {
              $("#the-string").hide();
           });
           e.preventDefault();
         });

       });
