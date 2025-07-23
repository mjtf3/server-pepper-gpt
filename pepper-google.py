= [[https://is.muni.cz/auth/predmet/fi/pv277|PV277 Programming Applications for Social Robots]] =

[ [wiki:en/ProgrammingRobotsCourse/Introduction previous part] ]  [ [wiki:en/ProgrammingRobotsCourse/PepperApi#PepperAPIII next part] ]

== Pepper API

[[PageOutline(2-3)]]

* http://doc.aldebaran.com/2-5/index_dev_guide.html

=== programming in Choregraphe via Python
  * enter only one box `Python Script`
  * edit its contents via double click:
    * to `onLoad` add:
      {{{#!python
self.tts = ALProxy('ALTextToSpeech')
self.tts.setLanguage('Czech')
}}}
    * to `onInput_onStart` add:
      {{{#!python
self.tts.say("Ahoj, jak se máš?")
self.onStopped()
}}}
   * add `Czech` into Project Properties [[br]]
     [[Image(pepper_project_cz.png)]]
   * save the project and run in on a virtual robot
 * for details see http://doc.aldebaran.com/2-5/software/choregraphe/objects/python_script.html and http://doc.aldebaran.com/2-5/software/choregraphe/reference.html

=== speech input via Python
  * in `onLoad` add (leave the `self.tts` lines from previous example there):
    {{{#!python
        self.dialog = ALProxy('ALDialog')
        self.dialog.setLanguage('Czech')
        self.mem = ALProxy('ALMemory')
        try:
            self.speech = ALProxy("ALSpeechRecognition")
            self.speech.setLanguage('Czech')
            self.logger.info('Running on real robot')
        except:
            self.logger.info('Running on virtual robot')
            self.speech = None
}}}
  * add at the very beginning of the Python code
    {{{#!python
import random
}}}
  * process speech accordingly
    {{{#!python
    def get_answer(self, reactions):
        if self.speech is None:
            # random answer on virtual robot
            return (random.choice(reactions.keys()))
        else:
            try:
                self.speech.setVocabulary(reactions.keys(), False)
            except RuntimeError: # fix incorrectly reset dialog
                self.logger.info('Reset language')
                self.dialog.setLanguage('Czech')
                self.onLoad()
                self.speech.setVocabulary(reactions.keys(), False)
            self.speech.subscribe("Test_ASR")
            self.logger.info('Speech recognition engine started')
            while True:
                word = self.mem.getData("WordRecognized")
                if type(word) == list and word[0] != '':
                    break
            self.speech.unsubscribe("Test_ASR")
            return word[0]

    def onInput_onStart(self):
        self.tts.say("Ahoj, jak se máš?")
        reactions = {
            'dobře':  'to je super!',
            'špatně': 'doufám, že to brzo bude lepší',
            'nevím': 'tak to určitě nebude tak zlé',
        }
        answer = self.get_answer(reactions)
        react = reactions.get(answer)
        self.logger.info('answer={}, react={}'.format(answer, react))
        self.tts.say(react)
        self.onStopped()
}}}
  * in case of error `ALSpeechRecognition::setVocabulary 		NuanceContext::addContext 	A grammar named "modifiable_grammar" already exists` just rerun the app once more. But this should be already solved by the included "''fix incorrectly reset dialog''".
  * see [http://doc.aldebaran.com/2-5/naoqi/audio/alspeechrecognition.html ALSpeechRecognition] documentation

=== dialog    
* add boxes `Set Language` with `Czech` and add `Czech` to project properties
* right click the free area -> `Create a new box` -> `Dialog...`
* in the Dialog -> `Add Topic` - choose `Czech` and `Add to the package content as collaborative dialog` (allows to start the dialog just by talking to the robot)
* connect `onStart` -> `Set Language` -> `Dialog`
* in Project files double click on `dialog_czc.top` and enter
  {{{
topic: ~dialog()
language: czc

concept:(ahoj) "ahoj robote"
concept:(dobrý_den) ["dobrý den" "krásný den" "krásný den přeju"]

u:(~ahoj) ahoj člověče
  \pau=1000\
  to máme dnes hezký den

u:(~dobrý_den) ~dobrý_den
}}}
* see [http://doc.aldebaran.com/2-5/naoqi/interaction/dialog/dialog.html QiChat - Introduction] and [http://doc.aldebaran.com/2-5/naoqi/interaction/dialog/dialog-syntax_full.html QiChat - Syntax] for details
* beware that the "nice" function of recognizing any text via `_*` is unfortunately not available in the real robot - free speech recognition works only as a payed service over-the-network. The dialog must use predefined (possibly dynamic) concepts instead via `_~conceptName`.

=== adding animations

1. single animation - via `Animation` box
1. connect to dialog:
  * add rule to topic:
    {{{
u:(["můžeš zamávat" zamávej] {prosím}) ahojky $zamavej=1
}}}
  * add [http://doc.aldebaran.com/2-5/software/choregraphe/objects/box_input_output.html#choregraphe-reference-box-output output] to the dialog box (right click -> Edit box) named `zamavej` (Bang, punctual)
  * add `Kisses` animation box, connect it to the `zamavej` output
1. within the dialog:
    {{{
u:(~ahoj) ^start(animations/Stand/Gestures/Hey_1) ahoj člověče
  \pau=1000\
  to máme dnes hezký den 
  ^wait(animations/Stand/Gestures/Hey_1)
}}}
    shows only on real robot, see [http://doc.aldebaran.com/2-5/naoqi/motion/alanimationplayer-advanced.html#animationplayer-list-behaviors-pepper default list of animations]

[ [wiki:en/ProgrammingRobotsCourse/Introduction previous part] ]  [ [wiki:en/ProgrammingRobotsCourse/PepperApi#PepperAPIII next part] ]

== Pepper API II

[ [wiki:en/ProgrammingRobotsCourse/PepperApi previous part] ]  [ [wiki:en/ProgrammingRobotsCourse/GettingWwwInfo next part] ]

[[PageOutline(2-3)]]

=== Live examples

==== Using basic arithmetics

See video [https://nlp.fi.muni.cz/trac/pepper/wiki/NlpPepperShows#IcandocomputationsinCzechUm%C3%ADmpo%C4%8D%C3%ADtatv%C4%8De%C5%A1tin%C4%9B "I can do computations " in Czech / "Umím počítat" v češtině].

See https://gitlab.fi.muni.cz/nlp/dialog_counting/ app for details.
Concepts for arithmetic operators and numbers are created. Not every number is defined, but rather decimal places and their combination, eg.

{{{
concept:(tens) [20 30 40 50 60 70 80 90]
concept:(number_hundreds) ["{[1 "jedno"]} sto" 
    "dvě stě" dvěsta dvěstě 
    "[3 4] sta" "[5 6 7 8 "osum" 9] set" pěcet šescet devěcet]
concept:(number) ["~number_hundreds {~number_tens} {~digits}" 
    "~number_tens {~digits}" ~digits]
}}}

This way, robot can understand numbers up to 999. Concepts are used in the dialogue, passed into counting function and output result is said in the dialogue:

{{{
u:(["kolik je" spočítej] _"~number ~operator [~number ~number2]")
    $num_expression=$1
    ^call(ALDialogCounting.compute($num_expression))
    c1:(_* equals nan) $1 přece nejde spočítat!
    c1:(_* equals _*) $1 [je "by mohlo být"] {asi} {tak} $2

}}}

The computing function receives the recognized words as parameters and has to convert the words to numbers and operation before producing the result. The `command` parameter contains recognized sentence, eg. "dvacet dva plus třináct".

{{{#!python
m = re.match('(.*) (' + '|'.join(OPERATOR_WORDS) + ') (.*)', command)
if m:
  number1 = self.convert_number(m.group(1))
  operator_word = m.group(2)
  operator = OPERATOR_WORDS[operator_word]
  number2 = self.convert_number(m.group(3))
  try:
    result = str(int(eval(str(number1) + operator + str(number2)))).replace('-','minus')
   except:
     result = 'nan'
}}}

==== Display subtitles for speech recognition/generation
See video [https://nlp.fi.muni.cz/trac/pepper/wiki/NlpPepperShows#subtitlesandlanguageswitchingbetweenCzechandEnglishtitulkyap%C5%99ep%C3%ADn%C3%A1n%C3%ADmezi%C4%8De%C5%A1tinouaangli%C4%8Dtinou Subtitles and language switching between Czech and English / titulky a přepínání mezi češtinou a angličtinou].

The subtitle service is running as an HTML app on the Pepper's tablet, receiving updates via Javascript messaging API. See https://gitlab.fi.muni.cz/nlp/dialog_subtitles/ app, specifically `dialog_subtitles/html/js/`.

HTML app can subscribe to various robot API events:

{{{#!javascript
RobotUtils.subscribeToALMemoryEvent("SpeechDetected", onSpeechDetected);
RobotUtils.subscribeToALMemoryEvent("ALSpeechRecognition/Status", onSpeechStatus);
RobotUtils.subscribeToALMemoryEvent("WordRecognizedAndGrammar", onWordRecognized);
}}}

And update the webpage when events are triggered, eg. display recognized word:

{{{#!javascript
function onWordRecognized(value)
{
    document.getElementById("word").innerHTML = value;
}
}}}

==== Access timetable API

See video [https://nlp.fi.muni.cz/trac/pepper/wiki/NlpPepperShows#PublictransportinCzechj%C3%ADzdn%C3%AD%C5%99%C3%A1dv%C4%8De%C5%A1tin%C4%9B Public transport in Czech / jízdní řád v češtině].

See `kordisbot` app (in the directory `/nlp/projekty/pepper/myapps`) for detailed example. To enable recognition of all stops and street names, special concepts were defined (`Ulice-concept.top` and `Zastavky-concept.top`) with the list of accepted names.

Timetable search is running as a service, see `scripts/kordisbot_service.py`. With a user's question, the dialog just calls specific service function, eg.

{{{
u:("[řekni ukaž zobraz najdi] {mi} [odjezdy spoje] ze zastávky _~station_name na zastávku _~station_name")
    ^call(DialogKordisbot.say_answer2($1,$2,1))
}}}

The service functions `say_answer1` and `say_answer2` are directly generating robot answer sentence.

Connection map is displayed on the tablet, using usual map from `mapy.idos.cz` with the connection parameters:

{{{
self.s.ALTabletService.showWebview("http://mapy.idos.cz/idsjmk/?f={}&t={}&date={}&time={}&submit=true".format(
fromStop, toStop, date, time))
}}} 

==== Pepper usage around the world:

 * Teaching assistant https://youtu.be/tBDI6kjj4nI
 * Care assistant https://youtu.be/XuwP5iOB-gs
 * Shop assistant https://youtu.be/iJ184evAu-I
 * Bank assistant https://youtu.be/norC0ekdoLQ

=== installing application to the robot
  * go to `aurora.fi.muni.cz`, build and copy your SSH keys for the robot access (replace `<xlogin>` with your login):
    {{{
ssh <xlogin>@aurora.fi.muni.cz
}}}
  * make a ssh key (again replace `<xlogin>` with your login):
    {{{
ssh-keygen -m PEM -t ecdsa -N '' -f ~/.ssh/pepper_<xlogin>
}}}
  * copy your '''public''' key to the course directory:
    {{{
cp ~/.ssh/pepper_<xlogin>.pub /nlp/projekty/pepper/course/keys/
}}}
  * add host `karel` to your `$HOME/.ssh/config`:
    {{{
Host karel
    User nao
    HostName 192.168.88.10
    # IdentityFile is important for install_pkg.py
    IdentityFile ~/.ssh/pepper_<xlogin>
    StrictHostKeyChecking no
    PubkeyAuthentication yes
}}}
  * build the PKG package in Choregraphe
  * test [https://nlp.fi.muni.cz/trac/pepper/wiki/LogView logview]
    {{{
ssh aurora
/nlp/projekty/pepper/bin/logview
}}}
  * after the key is allowed, install it to the robot
    {{{
ssh aurora
/nlp/projekty/pepper/bin/install_pkg.py your_package.pkg
}}}
=== running/launching the application

  * if the application contains a ''behavior'' (`behavior.xar`), it needs to be ''launched''. Behaviors can have two natures: ''interactive'' (used as a dialog) or ''solitary'' (used without a direct listener). Any behavior can be launched using one of 3 ways:
      1. specify the behavior's '''[http://doc.aldebaran.com/2-5/naoqi/interaction/triggerconditions.html trigger conditions]''' (works with both [http://doc.aldebaran.com/2-5/software/choregraphe/tutos/create_solitary_activity.html solitary] and [http://doc.aldebaran.com/2-5/software/choregraphe/tutos/create_interactive_activity.html interactive]) and/or its [http://doc.aldebaran.com/2-5/software/choregraphe/tutos/create_interactive_activity.html#step-2-transform-it-into-an-interactive-activity trigger sentences]
      1. run it with `run_app.py`:
    {{{
/nlp/projekty/pepper/bin/run_app.py your_package[/path_to_behavior]
}}}
         call `run_app.py -l` to obtain a list of installed behaviors.
      1. call ''[http://doc.aldebaran.com/2-5/naoqi/interaction/autonomouslife-api.html#ALAutonomousLifeProxy::switchFocus ALAutonomousLife.switchFocus]'' or !QiChat [http://doc.aldebaran.com/2-5/naoqi/interaction/dialog/dialog-syntax_full.html#switchfocus ^switchFocus]

=== using tablet
  * from a dialogue (see [http://doc.aldebaran.com/2-5/getting_started/creating_applications/using_peppers_tablet.html QiChat - pCall]):
    {{{
u:(jak se můžu dostat na fakultu bez přijímaček?)
    Způsobů je celá řada. 
    ^pCall(ALTabletService.showWebview("https://www.fi.muni.cz/admission/guide.html.cs"))
    Všechno se dozvíš dnes na přednášce, od paní ze studijního
    ^start(animations/Stand/Gestures/ShowTablet_3)
    nebo na webu vvv fi muni cz v sekci pro uchazeče.
    ^wait(animations/Stand/Gestures/ShowTablet_3)
}}}
  * application specific content can be displayed when stored in the subdirectory `html` and (after installation on the real robot) referred from the tablet as `http://198.18.0.1/apps/<application_name>/...`. This way not only images, but also HTML pages with !JavaScript content can be presented. The !JavaScript can also communicate with robot variables in real time, see [https://gitlab.fi.muni.cz/nlp/dialog_presentation_nlp dialog_presentation_nlp] for an example.
  * [http://doc.aldebaran.com/2-5/getting_started/creating_applications/using_peppers_tablet.html Using Pepper’s Tablet]

=== face characteristics

* [http://doc.aldebaran.com/2-5/software/choregraphe/tutos/get_age.html Get Age]/Get Gender
* [http://doc.aldebaran.com/2-5/software/choregraphe/tutos/get_expression.html Get Expression]

=== creating application outside Choregraphe

  * prepare your `pepper` directory unless you already have one
    {{{
mkdir $HOME/pepper
}}}
  * copy `template` directory
    {{{
cp -r /nlp/projekty/pepper/course/template $HOME/pepper/
}}}
  * rename the `template` to `template_<xlogin>` (replace `<xlogin>` with your login) or something else:
    {{{
mv $HOME/pepper/template $HOME/pepper/template_<xlogin>
cd $HOME/pepper/template_<xlogin>
}}}
  * go through all files, rename the application where necessary
  * build the PKG package (the version number will be increased):
    {{{
cd $HOME/pepper/template_<xlogin>
make pkg
}}}
  * and install it
    {{{
cd $HOME/pepper/template_<xlogin>
make install
}}}
    During the development this can be in one command
    {{{
make pkg install
}}}

=== creating own service

  * copy and rename `template-service` directory
    {{{
cp -r /nlp/projekty/pepper/course/template-service $HOME/pepper/
mv $HOME/pepper/template-service $HOME/pepper/template-service_<xlogin>
cd $HOME/pepper/template-service_<xlogin>
}}}
  * go through all files, rename the application where necessary
  * build the PKG and install it


[[br]]

[ [wiki:en/ProgrammingRobotsCourse/PepperApi previous part] ]  [ [wiki:en/ProgrammingRobotsCourse/GettingWwwInfo next part] ]

