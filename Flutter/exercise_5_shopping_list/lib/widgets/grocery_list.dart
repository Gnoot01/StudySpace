import 'dart:convert';

import 'package:exercise_5_shopping_list/data/categories.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import 'package:exercise_5_shopping_list/models/grocery_item.dart';
import 'package:exercise_5_shopping_list/widgets/new_item.dart';

class GroceryList extends StatefulWidget {
  const GroceryList({super.key});

  @override
  State<GroceryList> createState() => _GroceryListState();
}

class _GroceryListState extends State<GroceryList> {
  List<GroceryItem> _groceryItems = [];
  var _isLoading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadItems();
  }

  void _loadItems() async {
    try {
      final response = await http.get(
        Uri.https(
            "flutter-prep-default-rtdb.firebaseio.com", "shopping-list.json"),
      );
      if (response.statusCode >= 400) {
        // All errors
        setState(() {
          _error = "Failed to fetch data. Please try again later!";
        });
      }

      if (response.body == 'null') {
        setState(() {
          _isLoading = false;
        });
        return;
      }

      final Map<String, dynamic> listData = json.decode(response.body);
      final List<GroceryItem> loadedItems = [];
      for (final item in listData.entries) {
        final category = categories.entries
            .firstWhere(
              (catItem) => catItem.value.title == item.value["category"],
            )
            .value;
        loadedItems.add(
          GroceryItem(
              id: item.key,
              name: item.value['name'],
              quantity: item.value['quantity'],
              category: category),
        );
      }
      setState(() {
        _groceryItems = loadedItems;
        _isLoading = false;
      });
    } catch (error) {
      setState(() {
        _error = "Something went wrong! Please try again later!";
      });
    }
  }

  void _addItem() async {
    final newItem = await Navigator.of(context).push<GroceryItem>(
      MaterialPageRoute(
        builder: (ctx) => const NewItem(),
      ),
    );

    _loadItems();

    // Can return to GroceryList Screen also by tapping back button,
    //  in which case newItem = null
    if (newItem == null) {
      return;
    }

    setState(() {
      _groceryItems.add(newItem);
    });
  }

  void _removeItem(GroceryItem item) async {
    final index = _groceryItems.indexOf(item);
    setState(() {
      _groceryItems.remove(item);
    });
    final response = await http.delete(
      Uri.https("flutter-prep-default-rtdb.firebaseio.com",
          "shopping-list/${item.id}.json"),
    );

    if (response.statusCode >= 400) {
      setState(() {
        _groceryItems.insert(index, item);
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    Widget content = const Center(child: Text('No items added yet.'));

    if (_isLoading) {
      // loading spinner
      content = const Center(
        child: CircularProgressIndicator(),
      );
    }

    if (_groceryItems.isNotEmpty) {
      content = ListView.builder(
        itemCount: _groceryItems.length,
        itemBuilder: (ctx, index) => Dismissible(
          onDismissed: (direction) {
            _removeItem(_groceryItems[index]);
          },
          key: ValueKey(_groceryItems[index].id),
          child: ListTile(
            title: Text(_groceryItems[index].name),
            leading: Container(
              width: 24,
              height: 24,
              color: _groceryItems[index].category.color,
            ),
            trailing: Text(
              _groceryItems[index].quantity.toString(),
            ),
          ),
        ),
      );
    }

    if (_error != null) {
      content = Center(
        child: Text(_error!),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Your Groceries'),
        actions: [
          IconButton(
            onPressed: _addItem,
            icon: const Icon(Icons.add),
          ),
        ],
      ),
      body: content,
    );
  }
}

// // For FutureBuilder
//   Future<List<GroceryItem>> _loadItems() async {
//     final response = await http.get(
//       Uri.https(
//           "flutter-prep-default-rtdb.firebaseio.com", "shopping-list.json"),
//     );
//     if (response.statusCode >= 400) {
//       throw Exception("Failed to fetch data. Please try again later!");
//     }

//     if (response.body == 'null') {
//       return [];
//     }

//     final Map<String, dynamic> listData = json.decode(response.body);
//     final List<GroceryItem> loadedItems = [];
//     for (final item in listData.entries) {
//       final category = categories.entries
//           .firstWhere(
//             (catItem) => catItem.value.title == item.value["category"],
//           )
//           .value;
//       loadedItems.add(
//         GroceryItem(
//             id: item.key,
//             name: item.value['name'],
//             quantity: item.value['quantity'],
//             category: category),
//       );
//     }
//     return loadedItems;
//   }

//   void _addItem() async {
//     final newItem = await Navigator.of(context).push<GroceryItem>(
//       MaterialPageRoute(
//         builder: (ctx) => const NewItem(),
//       ),
//     );

//     _loadItems();

//     // Can return to GroceryList Screen also by tapping back button,
//     //  in which case newItem = null
//     if (newItem == null) {
//       return;
//     }

//     setState(() {
//       _groceryItems.add(newItem);
//     });
//   }

//   void _removeItem(GroceryItem item) async {
//     final index = _groceryItems.indexOf(item);
//     setState(() {
//       _groceryItems.remove(item);
//     });
//     final response = await http.delete(
//       Uri.https("flutter-prep-default-rtdb.firebaseio.com",
//           "shopping-list/${item.id}.json"),
//     );

//     if (response.statusCode >= 400) {
//       setState(() {
//         _groceryItems.insert(index, item);
//       });
//     }
//   }

//   @override
//   Widget build(BuildContext context) {

//     return Scaffold(
//       appBar: AppBar(
//         title: const Text('Your Groceries'),
//         actions: [
//           IconButton(
//             onPressed: _addItem,
//             icon: const Icon(Icons.add),
//           ),
//         ],
//       ),
//       // Updating UI based on state of Future
//       // GOOD PRACTICE: _loadedItems, not _loadItems() as will be re-executed everytime
//       body: FutureBuilder(
//         future: _loadedItems,
//         builder: (context, snapshot) {
//           // Waiting for response after sending request
//           if (snapshot.connectionState == ConnectionState.waiting) {
//             return const Center(
//               child: CircularProgressIndicator(),
//             );
//           }
//           // Error thrown
//           if (snapshot.hasError) {
//             return Center(
//               child: Text(snapshot.error.toString()),
//             );
//           }

//           if (snapshot.data!.isEmpty) {
//             return const Center(
//               child: Text('No items added yet.'),
//             );
//           }

//           return ListView.builder(
//             itemCount: snapshot.data!.length,
//             itemBuilder: (ctx, index) => Dismissible(
//               onDismissed: (direction) {
//                 _removeItem(snapshot.data![index]);
//               },
//               key: ValueKey(snapshot.data![index].id),
//               child: ListTile(
//                 title: Text(snapshot.data![index].name),
//                 leading: Container(
//                   width: 24,
//                   height: 24,
//                   color: snapshot.data![index].category.color,
//                 ),
//                 trailing: Text(
//                   snapshot.data![index].quantity.toString(),
//                 ),
//               ),
//             ),
//           );
//         },
//       ),
//     );
//   }
// }
