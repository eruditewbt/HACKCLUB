import 'dart:convert';
import 'dart:io';

/// Run with:
///   dart replace_with_localizations.dart [--auto]
///
/// Looks through lib/screens for quoted UI strings and replaces them with
/// `AppLocalizations.of(context).key ?? 'key'`.
///
/// Options:
///   --auto   Apply replacements automatically without prompts.

Future<void> main(List<String> args) async {
  final autoReplace = args.contains('--auto');

  final arbFile = File('lib/l10n/app_en.arb');
  if (!await arbFile.exists()) {
    print('❌ Missing: ${arbFile.path}');
    exit(1);
  }

  final Map<String, dynamic> arbContent =
      json.decode(await arbFile.readAsString());
  final translations = <String, String>{};
  arbContent.forEach((key, value) {
    if (!key.startsWith('@')) translations[value.toString()] = key;
  });

  final libDir = Directory('lib/screens');
  if (!await libDir.exists()) {
    print('❌ Missing directory: ${libDir.path}');
    exit(1);
  }

  print('🔍 Scanning ${libDir.path} …\n');
  int total = 0, changed = 0;

  await for (final entity in libDir.list(recursive: true)) {
    if (entity is! File || !entity.path.endsWith('.dart')) continue;
    total++;

    var text = await entity.readAsString();
    var newText = text;
    var edits = 0;

    for (final pattern in [
      RegExp(r"'((?:\\.|[^\\'])*?)'", dotAll: true),
      RegExp(r'"((?:\\.|[^\\"])*?)"', dotAll: true),
    ]) {
      final (updated, count) = await _processMatches(
          entity.path, newText, pattern, translations, autoReplace);
      newText = updated;
      edits += count;
    }

    if (newText != text) {
      // optional one-line backup
      await File('${entity.path}.bak').writeAsString(text);
      await entity.writeAsString(newText);
      changed++;
      print('✅ Updated: ${entity.path} ($edits changes)');
    } else {
      print('⚪ No changes: ${entity.path}');
    }
  }

  print('\n🏁 Done. Files scanned: $total | Updated: $changed');
}

Future<(String, int)> _processMatches(
  String filePath,
  String content,
  RegExp regex,
  Map<String, String> translations,
  bool autoReplace,
) async {
  final matches = regex.allMatches(content).toList();
  var updated = content;
  var count = 0;

  final sorted = translations.entries.toList()
    ..sort((a, b) => b.key.length.compareTo(a.key.length));

  for (final m in matches.reversed) {
    final full = m.group(0)!;
    final inner = m.group(1)!;
    final trimmed = inner.trim();
    if (trimmed.isEmpty || _looksLikeCodeOrVariable(trimmed)) continue;

    String? key;
    String replacement = inner;

    // Prefer full match first
    final fullEntry = sorted.firstWhere(
      (e) => e.key.trim() == trimmed,
      orElse: () => const MapEntry('', ''),
    );

    if (fullEntry.key.isNotEmpty) {
      key = fullEntry.value;
      replacement = r'${(AppLocalizations.of(context)?.' + '$key ?? \'$key\')}';
    } else {
      // Fallback: longest substring
      for (final e in sorted) {
        if (inner.contains(e.key)) {
          key = e.value;
          replacement = inner.replaceAll(
            e.key,
            r'${(AppLocalizations.of(context)?.' + '$key ?? \'${e.value}\')}',
          );
          break;
        }
      }
    }

    if (key == null) continue;

    final quote = full.startsWith("'") ? "'" : '"';
    print('\n📄 $filePath');
    print('Found: "$inner"');
    print('→ Suggest: $quote$replacement$quote');

    var replace = autoReplace;
    if (!autoReplace) {
      stdout.write('Replace? (y/n): ');
      replace = (stdin.readLineSync()?.trim().toLowerCase() == 'y');
    }

    if (replace) {
      updated =
          updated.replaceRange(m.start, m.end, '$quote$replacement$quote');
      count++;
      print('✅ Replaced.');
    } else {
      print('⏭️ Skipped.');
    }
  }

  return (updated, count);
}

bool _looksLikeCodeOrVariable(String s) =>
    s.startsWith('http') ||
    s.startsWith('import ') ||
    s.startsWith('package:') ||
    s.startsWith('\$') ||
    s.contains(RegExp(r'[(){}=><]')) ||
    s.contains('print(') ||
    s.contains('const ') ||
    s.contains('final ') ||
    s.contains('=>');
