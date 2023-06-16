import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:exercise_2_quiz/questions.dart';
import 'package:exercise_2_quiz/qns_summary/qns_summary.dart';

class ResultsScreen extends StatelessWidget {
  const ResultsScreen(this.chosenAns, this.onRestart, {super.key});

  final List<String> chosenAns;
  final void Function() onRestart;

  // Getter: "getting a value", used as a property, internally is a method
  List<Map<String, Object>> get summary {
    final List<Map<String, Object>> summary = [];

    for (var i = 0; i < chosenAns.length; i++) {
      summary.add({
        "qn_index": i,
        "qn": questions[i].text,
        "correct_ans": questions[i].answers[0],
        "user_ans": chosenAns[i],
      });
    }
    return summary;
  }

  @override
  Widget build(BuildContext context) {
    final numTotalQns = questions.length;
    // Arrow funciton = Anonymous + 1 liner (Diff from JS)
    final numCorrectQns =
        summary.where((data) => data["user_ans"] == data["correct_ans"]).length;

    return Center(
      child: Container(
        margin: const EdgeInsets.all(20),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              "$numCorrectQns out of $numTotalQns correct!",
              style: GoogleFonts.lato(
                color: const Color.fromARGB(255, 230, 200, 253),
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 30),
            QnsSummary(summary),
            const SizedBox(
              height: 30,
            ),
            TextButton.icon(
              onPressed: onRestart,
              style: TextButton.styleFrom(
                foregroundColor: Colors.white,
              ),
              icon: const Icon(Icons.refresh),
              label: const Text('Restart Quiz!'),
            )
          ],
        ),
      ),
    );
  }
}
