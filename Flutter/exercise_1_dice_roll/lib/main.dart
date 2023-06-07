import 'package:flutter/material.dart';
import 'package:exercise_1_dice_roll/gradient_container.dart';

void main() {
  runApp(
    const MaterialApp(
      home: Scaffold(
        body: GradientContainer([Colors.cyan, Color.fromARGB(1, 157, 182, 69)]),
      ),
    ),
  );
}
