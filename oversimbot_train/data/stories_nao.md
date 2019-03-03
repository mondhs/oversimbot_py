## story_0phase_happy_path
* greet <!--user says hi-->
 - utter_welcomeback
 - utter_whats_your_name
* my_name_is{"person_name":"Mindas"} <!--user introduces him/her self-->
 - action_check_name <!-- Unclear if name is missing  -->
 - utter_nao_intro
 - utter_do_you_like_travel
* affirm
 - utter_how_do_you_like_travel <!-- by what transportation options user prefers-->
* prefered_travel_option
 - action_transportation_options
 - utter_respond_on_travel_option
 - utter_ask_what_is_first_obstacle
* identify_first_obstacle
 - action_identify_first_obstacle
 - utter_first_obstacle_correct
 - utter_second_chalange_hints
 - utter_second_chalange
* identify_second_chalange
 - action_identify_second_chalange
 - utter_second_chalange_correct
 - utter_bye
* bye
 - utter_bye


## story_0phase_unhappy_path
* greet <!--user says hi-->
 - utter_welcomeback
 - utter_whats_your_name
* my_name_is{"person_name":"Mindas"} <!--user introduces him/her self-->
 - action_check_name <!-- Unclear if name is missing  -->
 - utter_nao_intro
 - utter_do_you_like_travel
* deny OR dont_know
 - action_dont_travel
