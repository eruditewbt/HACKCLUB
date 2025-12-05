import 'dart:io';
import 'package:yaml/yaml.dart';
import 'package:translate_tool_v3/src/core.dart';

void runCli(List<String> args) async {
  final file = File('translate_tool.yaml');
  if (!await file.exists()) {
    print('⚙️  Creating default translate_tool.yaml...');
    await file.writeAsString(defaultYamlConfig);
  }

  final yaml = loadYaml(await file.readAsString());
  final config = Map<String, dynamic>.from(yaml);

  if (args.isEmpty) {
    print('Usage: dart run translate_tool_v3 <extract|merge|replace|sync|web>');
    exit(0);
  }

  switch (args.first) {
    case 'extract':
      await extractStrings(config);
      break;
    case 'replace':
      await replaceStrings(config);
      break;
    case 'merge':
      await mergeTranslations(config);
      break;
    case 'sync':
      await extractStrings(config);
      await mergeTranslations(config);
      break;
    case 'web':
      runWebEditor();
      break;
    default:
      print('Unknown command: ${args.first}');
  }
}
