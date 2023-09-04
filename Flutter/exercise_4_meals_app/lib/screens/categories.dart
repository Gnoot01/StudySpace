import 'package:exercise_4_meals_app/models/meal.dart';
import 'package:exercise_4_meals_app/screens/meals.dart';
import 'package:exercise_4_meals_app/widgets/category_grid_item.dart';
import 'package:flutter/material.dart';

import 'package:exercise_4_meals_app/data/dummy_data.dart';
import 'package:exercise_4_meals_app/models/category.dart';

class CategoriesScreen extends StatefulWidget {
  const CategoriesScreen({super.key, required this.availMeals});

  final List<Meal> availMeals;

  @override
  State<CategoriesScreen> createState() => _CategoriesScreenState();
}

class _CategoriesScreenState extends State<CategoriesScreen>
    with SingleTickerProviderStateMixin {
  // Won't have value at creation of class, but will have as soon as used
  late AnimationController _animationController;

  @override
  void initState() {
    super.initState();

    _animationController = AnimationController(
      // animation FPS (Default 60), animation value = 0-1 in 300ms
      vsync: this, duration: const Duration(milliseconds: 300), lowerBound: 0,
      upperBound: 1,
    );

    // Start animation
    _animationController.forward();
  }

  @override
  void dispose() {
    _animationController.dispose();
    super.dispose();
  }

  void _selectCategory(BuildContext context, Category category) {
    final filteredMeals = widget.availMeals
        .where((meal) => meal.categories.contains(category.id))
        .toList();

    // Adding to topmost screen, automatically comes with back button to pop topmost screen
    // Navigator.of(context).push(route)
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (ctx) => MealsScreen(
          title: category.title,
          meals: filteredMeals,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    // Listen to animation
    return AnimatedBuilder(
      animation: _animationController,
      // Static, built once
      child: GridView(
        padding: const EdgeInsets.all(24),
        // Gridview similar to Listview
        // Set no. of columns
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 2,
            childAspectRatio: 3 / 2,
            crossAxisSpacing: 20,
            mainAxisSpacing: 20),
        children: [
          for (final category in availableCategories)
            CategoryGridItem(
              category: category,
              onSelectCategory: () => _selectCategory(context, category),
            ),
        ],
      ),
      // Padding executed (rebuilt) every tick, refers to same child ^
      // builder: (context, child) => Padding(
      //   padding: EdgeInsets.only(top: 100 - _animationController.value * 100),
      //   child: child,
      // ),
      builder: (context, child) => SlideTransition(
          position: Tween(
            begin: const Offset(0, 0.3),
            end: const Offset(0, 0),
          ).animate(
            CurvedAnimation(
                parent: _animationController, curve: Curves.easeInOut),
          ),
          child: child),
    );
  }
}
