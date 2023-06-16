import 'package:flutter/material.dart';
import 'package:exercise_2_quiz/qns_summary/summary_item.dart';

class QnsSummary extends StatelessWidget {
  const QnsSummary(this.summary, {super.key});

  final List<Map<String, Object>> summary;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      // Need SizedBox + SingleChildScrollView for scrollable window
      height: 400,
      child: SingleChildScrollView(
        child: Column(
          children: summary.map((data) {
            return SummaryItem(data);
          }).toList(),
        ),
      ),
    );
  }
}
