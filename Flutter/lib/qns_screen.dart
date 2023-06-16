import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:exercise_2_quiz/ans_btn.dart';
import 'package:exercise_2_quiz/questions.dart';

class QnsScreen extends StatefulWidget {
  const QnsScreen(this.onSelectAns, {super.key});
  final void Function(String ans) onSelectAns;

  @override
  State<QnsScreen> createState() {
    return _QnsScreenState();
  }
}

class _QnsScreenState extends State<QnsScreen> {
  var currentQnIndex = 0;

  void answerQn(String selectedAns) {
    widget.onSelectAns(selectedAns);
    setState(() {
      currentQnIndex++;
    });
  }

  @override
  Widget build(BuildContext context) {
    final currentQn = questions[currentQnIndex];

    return Center(
      child: Container(
        margin: const EdgeInsets.all(20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          // mainAxis in Column is vertical, ∴ crossAxis is horizontal
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(
              currentQn.text,
              style: GoogleFonts.lato(
                  color: Colors.white,
                  fontSize: 24,
                  fontWeight: FontWeight.bold),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 30),
            ...currentQn.shuffledAns.map(
              (ans) {
                return AnsBtn(ans, () {
                  answerQn(ans);
                });
              },
            )
          ],
        ),
      ),
    );
  }
}
