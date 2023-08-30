import 'package:exercise_3_expense_tracker/widgets/chart/chart.dart';
import 'package:exercise_3_expense_tracker/widgets/expenses_list/expenses_list.dart';
import 'package:exercise_3_expense_tracker/models/expense_model.dart';
import 'package:exercise_3_expense_tracker/widgets/new_expense.dart';
import 'package:flutter/material.dart';

class Expenses extends StatefulWidget {
  const Expenses({super.key});

  @override
  State<Expenses> createState() {
    return _ExpensesState();
  }
}

class _ExpensesState extends State<Expenses> {
  final List<ExpenseModel> _registeredExpenses = [
    ExpenseModel(
        title: "Flutter Course",
        amount: 4.69,
        date: DateTime.now(),
        category: Category.work),
    ExpenseModel(
        title: "Barbie",
        amount: 17.50,
        date: DateTime.now(),
        category: Category.leisure),
  ];

  void _openAddExpenseOverlay() {
    // Overlay
    // context: related to the Expenses Stateless Widget, ctx: related to showModalBottomSheet
    showModalBottomSheet(
      // Avoid device features like camera affecting UI
      useSafeArea: true,
      // Take full available height
      isScrollControlled: true,
      context: context,
      builder: (ctx) => NewExpense(onAddExpense: _addExpense),
    );
  }

  void _addExpense(ExpenseModel expense) {
    setState(() {
      _registeredExpenses.add(expense);
    });
  }

  void _removeExpense(ExpenseModel expense) {
    final expenseIndex = _registeredExpenses.indexOf(expense);
    setState(() {
      _registeredExpenses.remove(expense);
    });
    // "Undo" notification
    ScaffoldMessenger.of(context).clearSnackBars();
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        action: SnackBarAction(
          label: "Undo",
          onPressed: () => setState(
            () => _registeredExpenses.insert(expenseIndex, expense),
          ),
        ),
        duration: const Duration(seconds: 3),
        content: const Text("Expense deleted."),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final screenwidth = MediaQuery.of(context).size.width;

    Widget mainContent = const Center(
      child: Text("No expenses found. Add some!"),
    );

    if (_registeredExpenses.isNotEmpty) {
      mainContent = ExpensesList(
        expenses: _registeredExpenses,
        onRemoveExpense: _removeExpense,
      );
    }

    return Scaffold(
      // Row "ToolBar" at the top
      appBar: AppBar(title: const Text("Expense Tracker"), actions: [
        IconButton(
            onPressed: _openAddExpenseOverlay, icon: const Icon(Icons.add))
      ]),
      body: screenwidth < 600
          ? Column(
              children: [
                Chart(expenses: _registeredExpenses),
                Expanded(child: mainContent),
              ],
            )
          : Row(
              children: [
                // ALWAYS use Expanded when 2 nested Widgets take as much as space possible (no constraints)
                // Eg. Row with Textfield, Chart
                Expanded(
                  child: Chart(expenses: _registeredExpenses),
                ),
                Expanded(child: mainContent),
              ],
            ),
    );
  }
}
