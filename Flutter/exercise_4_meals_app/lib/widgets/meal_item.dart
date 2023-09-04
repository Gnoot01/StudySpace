import 'package:flutter/material.dart';
import 'package:transparent_image/transparent_image.dart';

import 'package:exercise_4_meals_app/widgets/meal_item_trait.dart';
import 'package:exercise_4_meals_app/models/meal.dart';

class MealItem extends StatelessWidget {
  const MealItem({
    super.key,
    required this.meal,
    required this.onSelectMeal,
  });

  final Meal meal;
  final void Function(Meal meal) onSelectMeal;

  String get complexityText {
    return meal.complexity.name[0].toUpperCase() +
        meal.complexity.name.substring(1);
  }

  String get affordabilityText {
    return meal.affordability.name[0].toUpperCase() +
        meal.affordability.name.substring(1);
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.all(8),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(8),
      ),
      // Ensures shape of parent persists despite stacked top children
      clipBehavior: Clip.hardEdge,
      // 3D shadow effect
      elevation: 2,
      child: InkWell(
        onTap: () => onSelectMeal(meal),
        // Stack Eg. text (child) on image (parent), starting with bottom (most background) layer
        child: Stack(
          children: [
            // Animate widget across diff screens
            Hero(
              tag: meal.id,
              // Fade in instead of popping in animation
              child: FadeInImage(
                // Dummy transparent image to ensure fading animation
                // Start animation: Image loaded from memory
                placeholder: MemoryImage(kTransparentImage),
                // End animation: Image loaded from internet
                image: NetworkImage(meal.imageUrl),
                // If image is too big to fit, it is cut off and zoomed in, not distorted
                fit: BoxFit.cover,
                height: 200,
                width: double.infinity,
              ),
            ),
            // Define how child should be positioned RELATIVE to parent on stack
            // At bottom, spanning left to right. If right = 50, child will end 50 pixels to the right before parent
            Positioned(
              bottom: 0,
              left: 0,
              right: 0,
              child: Container(
                color: Colors.black54,
                padding:
                    const EdgeInsets.symmetric(vertical: 6, horizontal: 44),
                child: Column(
                  children: [
                    Text(
                      meal.title,
                      maxLines: 2,
                      textAlign: TextAlign.center,
                      softWrap: true,
                      // Very long text -> ...
                      overflow: TextOverflow.ellipsis,
                      style: const TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    const SizedBox(height: 12),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        MealItemTrait(
                          icon: Icons.schedule,
                          label: '${meal.duration} min',
                        ),
                        const SizedBox(width: 12),
                        MealItemTrait(
                          icon: Icons.work,
                          label: complexityText,
                        ),
                        const SizedBox(width: 12),
                        MealItemTrait(
                          icon: Icons.attach_money,
                          label: affordabilityText,
                        )
                      ],
                    ),
                  ],
                ),
              ),
            )
          ],
        ),
      ),
    );
  }
}
