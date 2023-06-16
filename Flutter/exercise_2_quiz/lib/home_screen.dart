import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen(this.startQuiz, {super.key});

  final void Function() startQuiz;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // ❌ Opacity is performance-intensive!
          // Opacity(
          //   opacity: 0.65,
          //   child: Image.asset("assets/images/quiz-logo.png", width: 200),
          // ),
          Image.asset(
            "assets/images/quiz-logo.png",
            width: 200,
            // Smart alternative to opacity
            color: const Color.fromARGB(150, 255, 255, 255),
          ),
          const SizedBox(height: 80),
          const Text(
            "Learn Flutter the fun way!",
            style: TextStyle(color: Colors.white, fontSize: 24),
          ),
          const SizedBox(height: 30),
          // Alternative constructor for OutlinedButton with icon
          OutlinedButton.icon(
            onPressed: startQuiz,
            style: OutlinedButton.styleFrom(
                // foregroundColor = text color
                foregroundColor: Colors.white),
            icon: const Icon(Icons.arrow_right_alt_rounded),
            label: const Text(
              "Start Quiz",
            ),
          )
        ],
      ),
    );
  }
}
