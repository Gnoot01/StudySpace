import 'package:flutter/material.dart';
import 'package:exercise_1_dice_roll/dice_roller.dart';

class GradientContainer extends StatelessWidget {
  // Constructor function
  // superclass StatelessWidget wants some key for extra configuration, so any childclass must have too
  // : forwards any namedParameter key's value in GradientContainer to superclass StatelessWidget namedParameter key
  // const GradientContainer({key}) : super(key: key);
  const GradientContainer(this.colorList, {super.key});

  final List<Color> colorList;

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          // color gradient
          colors: colorList,
          // since Gradient is default left -> right
          begin: Alignment.bottomLeft,
          end: Alignment.topRight,
        ),
      ),
      child: const Center(
          // child: StyledText("Hiii"),
          // Column for stacking vertically, Row for beside horizontally
          child: DiceRoller()),
    );
  }
}
