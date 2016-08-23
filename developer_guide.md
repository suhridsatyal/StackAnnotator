Project Components
------------------
UI - code found in `assets`. Can be built using bower and grunt.
     A build task will create compiled static resources in `static` folder.
Backend - found inside standard Django app folders

Templating
----------
Compiled HTML of UI app can be treated as Django Templates.
i.e. Template path is set to `static` folder. 
As such, if a template is modified (in `assets` as per the norm),
the UI needs to be built as well.
