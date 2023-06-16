import 'package:exercise_2_quiz/quiz_qn.dart';

const questions = [
  QuizQn(
    'What are the main building blocks of Flutter UIs?',
    [
      'Widgets',
      'Components',
      'Blocks',
      'Functions',
    ],
  ),
  QuizQn('How are Flutter UIs built?', [
    'By combining widgets in code',
    'By combining widgets in a visual editor',
    'By defining widgets in config files',
    'By using XCode for iOS and Android Studio for Android',
  ]),
  QuizQn(
    'What\'s the purpose of a StatefulWidget?',
    [
      'Update UI as data changes',
      'Update data as UI changes',
      'Ignore data changes',
      'Render UI that does not depend on data',
    ],
  ),
  QuizQn(
    'Which widget should you try to use more often: StatelessWidget or StatefulWidget?',
    [
      'StatelessWidget',
      'StatefulWidget',
      'Both are equally good',
      'None of the above',
    ],
  ),
  QuizQn(
    'What happens if you change data in a StatelessWidget?',
    [
      'The UI is not updated',
      'The UI is updated',
      'The closest StatefulWidget is updated',
      'Any nested StatefulWidgets are updated',
    ],
  ),
  QuizQn(
    'How should you update data inside of StatefulWidgets?',
    [
      'By calling setState()',
      'By calling updateData()',
      'By calling updateUI()',
      'By calling updateState()',
    ],
  ),
  QuizQn(
    'What is Flutter?',
    [
      'A mobile app development framework',
      'A programming language',
      'A design pattern',
      'A software testing tool',
    ],
  ),
  QuizQn(
    'What are the main advantages of using Flutter?',
    [
      'Hot reload for instant code updates',
      'Cross-platform development (Android and iOS)',
      'Fast and smooth performance',
      'Rich set of pre-built UI components',
    ],
  ),
  QuizQn(
    'What is a widget in Flutter?',
    [
      'A building block for creating user interfaces',
      'A mathematical function',
      'A data structure',
      'A design pattern',
    ],
  ),
  QuizQn(
    'What is the difference between StatelessWidget and StatefulWidget?',
    [
      'StatelessWidget is immutable, while StatefulWidget can change its state',
      'StatelessWidget is for Android development, while StatefulWidget is for iOS development',
      'StatelessWidget is faster than StatefulWidget',
      'StatelessWidget requires less memory than StatefulWidget',
    ],
  ),
  QuizQn(
    'What is the purpose of the build() method in Flutter?',
    [
      'To define the structure and appearance of a widget',
      'To handle user interactions',
      'To fetch data from an API',
      'To perform animations',
    ],
  ),
  QuizQn(
    'What is the main function in a Flutter app?',
    [
      'The entry point of the application',
      'The function that handles network requests',
      'The function that defines the app\'s layout',
      'The function that triggers the build process',
    ],
  ),
  QuizQn(
    'What is the "hot reload" feature in Flutter?',
    [
      'The ability to see code changes instantly without restarting the app',
      'The process of optimizing app performance',
      'A feature for sharing app code with other developers',
      'A way to debug app crashes',
    ],
  ),
  QuizQn(
    'What is the pubspec.yaml file used for in a Flutter project?',
    [
      'To manage project dependencies',
      'To define the app\'s user interface',
      'To store user preferences',
      'To handle navigation between screens',
    ],
  ),
  QuizQn(
    'What is the purpose of the MaterialApp widget in Flutter?',
    [
      'To set up the basic app structure and navigation',
      'To handle user input and gestures',
      'To create animations and transitions',
      'To define the app\'s data models',
    ],
  ),
  QuizQn(
    "What is a StatefulWidget in Flutter?",
    [
      "A widget that can change its state during runtime",
      "A widget that is static and cannot be modified",
      "A widget that is used for layout purposes only",
      "A widget that handles user interactions",
    ],
  ),
  QuizQn(
    "What is the purpose of the initState() method in a StatefulWidget?",
    [
      "To initialize the state of the widget before it is displayed",
      "To handle user input and gestures",
      "To fetch data from an API",
      "To perform animations",
    ],
  ),
  QuizQn(
    "What is a GlobalKey used for in Flutter?",
    [
      "To uniquely identify a widget and access its state across different parts of the widget tree",
      "To handle navigation between screens",
      "To define the app's user interface",
      "To store user preferences",
    ],
  ),
  QuizQn(
    "What is the purpose of the const keyword in Flutter?",
    [
      "To create compile-time constant values that can be used in widget construction",
      "To indicate that a widget is stateful",
      "To optimize app performance",
      "To define the app's data models",
    ],
  ),
  QuizQn(
    "What is the difference between setState() and setState((){}) in Flutter?",
    [
      "setState() without arguments triggers a rebuild of the widget, while setState((){}) allows updating the widget's state",
      "setState() is used for widgets with a static state, while setState((){}) is used for widgets with a dynamic state",
      "setState() is a synchronous method, while setState((){}) is an asynchronous method",
      "There is no difference between the two, they can be used interchangeably",
    ],
  ),
  QuizQn(
    "What is the purpose of the FutureBuilder widget in Flutter?",
    [
      "To asynchronously fetch data from an API and update the UI when the data is available",
      "To handle user interactions and gestures",
      "To create animations and transitions",
      "To define the app's user interface",
    ],
  ),
  QuizQn(
    "What is the purpose of the GestureDetector widget in Flutter?",
    [
      "To detect and handle user gestures such as taps, swipes, and drags",
      "To manage project dependencies",
      "To set up the basic app structure and navigation",
      "To define the app's data models",
    ],
  ),
  QuizQn(
    "What is the purpose of the SingleChildScrollView widget in Flutter?",
    [
      "To provide a scrollable view for content that exceeds the screen size",
      "To optimize app performance",
      "To handle network requests",
      "To create responsive layouts for different screen sizes",
    ],
  ),
  QuizQn(
    "What is the purpose of the AnimatedContainer widget in Flutter?",
    [
      "To animate changes in its properties, such as size, position, and color",
      "To handle user input and gestures",
      "To define the app's user interface",
      "To fetch data from an API",
    ],
  ),
  QuizQn(
    "What is the purpose of the ShaderMask widget in Flutter?",
    [
      "To apply a shader to its child widget, allowing for custom visual effects",
      "To handle navigation between screens",
      "To store user preferences",
      "To create animations and transitions",
    ],
  ),
];
