import 'package:flutter/material.dart';
import 'dart:math';

// Good practice for memory efficiency, so new Random objects aren't created each time
final randomizer = Random();

// Dice need to change State, but don't require entire GradientContainer to be Stateful (overkill)
// StatefulWidgets require 2 classes
class DiceRoller extends StatefulWidget {
  const DiceRoller({super.key});

  @override
  State<DiceRoller> createState() {
    return _DiceRollerState();
  }
}

class _DiceRollerState extends State<DiceRoller> {
  int currentDiceRoll = 1;

  @override
  Widget build(BuildContext context) {
    return Column(
      // Default is max, giving as much space as possible (Squeezing to top)
      mainAxisSize: MainAxisSize.min,
      children: [
        Image.asset(
          "assets/images/dice-$currentDiceRoll.png",
          width: 200,
        ),
        // ElevatedButton for background color + shadow, OutlinedButton for no background color, TextButton for text
        TextButton(
          onPressed: () {
            // To re-execute build function, and show updated activeDiceImage
            setState(() {
              // (0 - 5) + 1 = (1 - 6)
              currentDiceRoll = randomizer.nextInt(6) + 1;
            });
          },
          style: TextButton.styleFrom(
              // Instead of padding, can create const SizedBox(height:20) b/w Image & TextButton
              padding: const EdgeInsets.only(top: 20),
              foregroundColor: Colors.white,
              textStyle: const TextStyle(fontSize: 28)),
          child: const Text("Roll Dice!"),
        )
      ],
    );
  }
}
