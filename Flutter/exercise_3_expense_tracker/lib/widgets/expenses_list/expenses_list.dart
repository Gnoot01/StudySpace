import 'package:exercise_3_expense_tracker/widgets/expenses_list/expense_item.dart';
import 'package:flutter/material.dart';
import 'package:exercise_3_expense_tracker/models/expense_model.dart';

class ExpensesList extends StatelessWidget {
  const ExpensesList(
      {super.key, required this.expenses, required this.onRemoveExpense});

  final List<ExpenseModel> expenses;
  final void Function(ExpenseModel expense) onRemoveExpense;

  @override
  Widget build(BuildContext context) {
    // Scrollable List, BUT only create when visible (scrolled into view) for performance
    return ListView.builder(
      itemCount: expenses.length,
      // Swipe to dismiss Widget
      itemBuilder: (ctx, index) => Dismissible(
        // Key to uniquely identify widget to dismiss
        key: ValueKey(expenses[index]),
        background: Container(
          color: Theme.of(context).colorScheme.error.withOpacity(0.75),
          margin: EdgeInsets.symmetric(
              horizontal: Theme.of(context).cardTheme.margin!.horizontal),
        ),
        onDismissed: (direction) => onRemoveExpense(expenses[index]),
        child: ExpenseItem(
          expenses[index],
        ),
      ),
    );
  }
}
