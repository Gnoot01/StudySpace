import 'package:flutter/material.dart';
import 'package:exercise_2_quiz/qns_screen.dart';
import 'package:exercise_2_quiz/questions.dart';
import 'package:exercise_2_quiz/home_screen.dart';
import 'package:exercise_2_quiz/results_screen.dart';

class Quiz extends StatefulWidget {
  const Quiz({super.key});

  @override
  State<Quiz> createState() {
    return _QuizState();
  }
}

class _QuizState extends State<Quiz> {
//   Widget? activeScreen;

//   void switchScreen() {
//     setState(() {
//       activeScreen = const QnsScreen();
//     });
//   }

// // ❌Widget activeScreen = HomeScreen(switchScreen) outside initState as simultaneously executed
// // ∴ switchScreen might not exist yet, so innate -> initState -> build
//   @override
//   void initState() {
//     activeScreen = HomeScreen(switchScreen);
//     super.initState();
//   }

//   @override
//   Widget build(BuildContext context) {
//     return MaterialApp(
//       home: Scaffold(
//         body: Container(
//             decoration: const BoxDecoration(
//               gradient: LinearGradient(
//                 colors: [
//                   Color.fromRGBO(103, 58, 183, 1),
//                   Color.fromARGB(255, 78, 13, 151)
//                 ],
//                 begin: Alignment.bottomLeft,
//                 end: Alignment.topRight,
//               ),
//             ),
//             child: activeScreen),
//       ),
//     );
//   }

  List<String> selectedAns = [];
  String activeScreen = "home-screen";

  void switchScreen() {
    setState(() {
      activeScreen = "qns-screen";
    });
  }

  void chooseAns(String ans) {
    selectedAns.add(ans);

    if (selectedAns.length == questions.length) {
      setState(() {
        activeScreen = "results-screen";
      });
    }
  }

  void restartQuiz() {
    setState(() {
      selectedAns = [];
      activeScreen = 'qns-screen';
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        body: Container(
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              colors: [
                Color.fromRGBO(103, 58, 183, 1),
                Color.fromARGB(255, 78, 13, 151)
              ],
              begin: Alignment.bottomLeft,
              end: Alignment.topRight,
            ),
          ),
          child: activeScreen == "home-screen"
              ? HomeScreen(switchScreen)
              : activeScreen == "results-screen"
                  ? ResultsScreen(selectedAns, restartQuiz)
                  : QnsScreen(chooseAns),
        ),
      ),
    );
  }
}
