import pytest
from unittest.mock import MagicMock, patch, call
from ara_cli.artefact_lister import ArtefactLister


@pytest.fixture
def artefact_lister():
    return ArtefactLister()


@pytest.mark.parametrize("artefact_content, artefact_path", [
    ("content1", "path1"),
    ("content2", "path2"),
    ("content3", "path3"),
])
def test_artefact_content_retrieval(artefact_content, artefact_path):
    # Mock the artefact object
    artefact_mock = MagicMock()
    artefact_mock.content = artefact_content
    artefact_mock.file_path = artefact_path

    # Test artefact_content_retrieval method
    content = ArtefactLister.artefact_content_retrieval(artefact_mock)
    assert content == artefact_content


@pytest.mark.parametrize("artefact_content, artefact_path", [
    ("content1", "path1"),
    ("content2", "path2"),
    ("content3", "path3"),
])
def test_artefact_path_retrieval(artefact_content, artefact_path):
    # Mock the artefact object
    artefact_mock = MagicMock()
    artefact_mock.content = artefact_content
    artefact_mock.file_path = artefact_path

    # Test artefact_path_retrieval method
    path = ArtefactLister.artefact_path_retrieval(artefact_mock)
    assert path == artefact_path


@pytest.mark.parametrize("tags, navigate_to_target", [
    (None, False),
    (["tag1", "tag2"], False),
    (["tag1"], True),
    ([], True)
])
@patch('ara_cli.artefact_lister.FileClassifier')
@patch('ara_cli.artefact_lister.DirectoryNavigator')
def test_list_files(mock_directory_navigator, mock_file_classifier, artefact_lister, tags, navigate_to_target):
    # Mock the DirectoryNavigator and its methods
    mock_navigator_instance = mock_directory_navigator.return_value
    mock_navigator_instance.navigate_to_target = MagicMock()

    # Mock the FileClassifier and its methods
    mock_classifier_instance = mock_file_classifier.return_value
    mock_classifier_instance.classify_files = MagicMock(return_value={'mocked_files': []})
    mock_classifier_instance.print_classified_files = MagicMock()

    # Call the method under test
    artefact_lister.list_files(tags=tags, navigate_to_target=navigate_to_target)

    # Verify that navigate_to_target was called if navigate_to_target is True
    if navigate_to_target:
        mock_navigator_instance.navigate_to_target.assert_called_once()
    else:
        mock_navigator_instance.navigate_to_target.assert_not_called()

    # Verify classify_files was called with the correct tags
    mock_classifier_instance.classify_files.assert_called_once_with(tags=tags)

    # Verify print_classified_files was called with the correct classified files
    mock_classifier_instance.print_classified_files.assert_called_once_with({'mocked_files': []})


@pytest.mark.parametrize("artefact_name, all_artefact_names, expected_output", [
    ("artefact1", ["artefact2", "artefact3"], ["No match found for artefact with name 'artefact1'"]),
    ("artefact1", ["artefact1", "artefact2"], [
        "No match found for artefact with name 'artefact1'",
        "Closest matches:",
        "  - artefact1",
        "  - artefact2"
    ]),
    ("artefact", ["artefac", "artefacto", "artifact"], [
        "No match found for artefact with name 'artefact'",
        "Closest matches:",
        "  - artefacto",
        "  - artefac",
        "  - artifact"
    ]),
    ("no_match", [], ["No match found for artefact with name 'no_match'"])
])
@patch('builtins.print')
def test_suggest_close_name_matches(mock_print, artefact_lister, artefact_name, all_artefact_names, expected_output):
    # Call the method under test
    artefact_lister.suggest_close_name_matches(artefact_name, all_artefact_names)

    # Prepare the expected calls
    expected_calls = [call(line) for line in expected_output]

    # Verify that print was called with the expected sequence of outputs
    mock_print.assert_has_calls(expected_calls, any_order=False)


@pytest.mark.parametrize("classifier, artefact_name, all_artefact_names", [
    ("classifier1", "artefact1", ["artefact2", "artefact3"]),
    ("classifier2", "artefact4", ["artefact5", "artefact6"]),
])
@patch('ara_cli.artefact_lister.FileClassifier')
def test_list_branch_name_not_found(mock_file_classifier, artefact_lister, classifier, artefact_name, all_artefact_names):
    # Mock the FileClassifier and its methods
    mock_classifier_instance = mock_file_classifier.return_value

    mock_artefacts = []
    for name in all_artefact_names:
        mock_artefact = MagicMock()
        mock_artefact.name = name
        mock_artefacts.append(mock_artefact)

    mock_classifier_instance.classify_files = MagicMock(return_value={classifier: mock_artefacts})

    # Mock suggest_close_name_matches to verify it's called
    artefact_lister.suggest_close_name_matches = MagicMock()

    # Call the method under test
    artefact_lister.list_branch(classifier=classifier, artefact_name=artefact_name)

    # Verify suggest_close_name_matches was called with the correct parameters
    artefact_lister.suggest_close_name_matches.assert_called_once_with(artefact_name, all_artefact_names)

@pytest.mark.parametrize("classifier, artefact_name, artefacts_by_classifier", [
    ("classifier1", "artefact1", {'classifier1': [{'name': 'artefact1', 'content': 'content1', 'file_path': 'path1'}]}),
])
@patch('ara_cli.artefact_lister.FileClassifier')
@patch('ara_cli.artefact_lister.ArtefactReader')
@patch('ara_cli.artefact_lister.filter_list')
def test_list_branch_success(mock_filter_list, mock_artefact_reader, mock_file_classifier, artefact_lister, classifier, artefact_name, artefacts_by_classifier):
    # Mock the FileClassifier and its methods
    mock_classifier_instance = mock_file_classifier.return_value

    mock_artefacts = []
    mock_artefact = MagicMock()
    mock_artefact.name = artefact_name.replace('_', ' ')
    mock_artefacts.append(mock_artefact)

    mock_classifier_instance.classify_files = MagicMock(return_value={classifier: mock_artefacts})
    mock_classifier_instance.print_classified_files = MagicMock()

    # Mock ArtefactReader's step_through_value_chain method
    mock_artefact_reader.step_through_value_chain = MagicMock()

    # Mock filter_list to simulate filtering
    mock_filter_list.return_value = artefacts_by_classifier

    # Call the method under test
    artefact_lister.list_branch(classifier=classifier, artefact_name=artefact_name)

    # Verify step_through_value_chain was called with the correct parameters
    mock_artefact_reader.step_through_value_chain.assert_called_once_with(
        artefact_name=artefact_name,
        classifier=classifier,
        artefacts_by_classifier={classifier: []}
    )

    # Verify filter_list was called with the correct parameters
    mock_filter_list.assert_called_once_with(
        {classifier: []},
        None,
        content_retrieval_strategy=ArtefactLister.artefact_content_retrieval,
        file_path_retrieval=ArtefactLister.artefact_path_retrieval
    )

    # Verify print_classified_files was called with the filtered artefacts
    mock_classifier_instance.print_classified_files.assert_called_once_with(artefacts_by_classifier)


@pytest.mark.parametrize("classifier, artefact_name, all_artefact_names", [
    ("classifier1", "artefact1", ["artefact2", "artefact3"]),
    ("classifier2", "artefact4", ["artefact5", "artefact6"]),
])
@patch('ara_cli.artefact_lister.FileClassifier')
def test_list_children_name_not_found(mock_file_classifier, artefact_lister, classifier, artefact_name, all_artefact_names):
    # Mock the FileClassifier and its methods
    mock_classifier_instance = mock_file_classifier.return_value
    mock_artefacts = []

    for name in all_artefact_names:
        mock_artefact = MagicMock()
        mock_artefact.name = name
        mock_artefacts.append(mock_artefact)

    mock_classifier_instance.classify_files = MagicMock(return_value={classifier: mock_artefacts})

    # Mock suggest_close_name_matches to verify it's called
    artefact_lister.suggest_close_name_matches = MagicMock()

    # Call the method under test
    artefact_lister.list_children(classifier=classifier, artefact_name=artefact_name)

    # Verify suggest_close_name_matches was called with the correct parameters
    artefact_lister.suggest_close_name_matches.assert_called_once_with(artefact_name, all_artefact_names)

@pytest.mark.parametrize("classifier, artefact_name, child_artefacts", [
    ("classifier1", "artefact1", [{'name': 'child1', 'content': 'content1', 'file_path': 'path1'}]),
])
@patch('ara_cli.artefact_lister.FileClassifier')
@patch('ara_cli.artefact_lister.ArtefactReader')
@patch('ara_cli.artefact_lister.filter_list')
def test_list_children_success(mock_filter_list, mock_artefact_reader, mock_file_classifier, artefact_lister, classifier, artefact_name, child_artefacts):
    # Mock the FileClassifier and its methods
    mock_classifier_instance = mock_file_classifier.return_value
    mock_artefacts = []

    mock_artefact = MagicMock()
    mock_artefact.name = artefact_name.replace('_', ' ')
    mock_artefacts.append(mock_artefact)

    mock_classifier_instance.classify_files = MagicMock(return_value={classifier: mock_artefacts})
    mock_classifier_instance.print_classified_files = MagicMock()

    # Mock ArtefactReader's find_children method
    mock_artefact_reader.find_children = MagicMock(return_value=child_artefacts)

    # Mock filter_list to simulate filtering
    mock_filter_list.return_value = child_artefacts

    # Call the method under test
    artefact_lister.list_children(classifier=classifier, artefact_name=artefact_name)

    # Verify find_children was called with the correct parameters
    mock_artefact_reader.find_children.assert_called_once_with(
        artefact_name=artefact_name,
        classifier=classifier
    )

    # Verify filter_list was called with the correct parameters
    mock_filter_list.assert_called_once_with(
        child_artefacts,
        None,
        content_retrieval_strategy=ArtefactLister.artefact_content_retrieval,
        file_path_retrieval=ArtefactLister.artefact_path_retrieval
    )

    # Verify print_classified_files was called with the filtered artefacts
    mock_classifier_instance.print_classified_files.assert_called_once_with(
        files_by_classifier=child_artefacts
    )


@pytest.mark.parametrize("classifier, artefact_name, all_artefact_names", [
    ("classifier1", "artefact1", ["artefact2", "artefact3"]),
    ("classifier2", "artefact4", ["artefact5", "artefact6"]),
])
@patch('ara_cli.artefact_lister.FileClassifier')
def test_list_data_name_not_found(mock_file_classifier, artefact_lister, classifier, artefact_name, all_artefact_names):
    # Mock the FileClassifier and its methods
    mock_classifier_instance = mock_file_classifier.return_value

    mock_artefacts = []
    for name in all_artefact_names:
        mock_artefact = MagicMock()
        mock_artefact.name = name
        mock_artefacts.append(mock_artefact)

    mock_classifier_instance.classify_files = MagicMock(return_value={classifier: mock_artefacts})

    # Mock suggest_close_name_matches to verify it's called
    artefact_lister.suggest_close_name_matches = MagicMock()

    # Call the method under test
    artefact_lister.list_data(classifier=classifier, artefact_name=artefact_name)

    # Verify suggest_close_name_matches was called with the correct parameters
    artefact_lister.suggest_close_name_matches.assert_called_once_with(artefact_name, all_artefact_names)


@pytest.mark.parametrize("classifier, artefact_name, content, file_path, does_exist", [
    ("classifier1", "artefact1", "content1", "path/to/artefact1.data", True),
    ("classifier2", "artefact2", "content2", "path/to/artefact2.data", False),
])
@patch('ara_cli.artefact_lister.FileClassifier')
@patch('ara_cli.artefact_lister.ArtefactReader')
@patch('ara_cli.artefact_lister.list_files_in_directory')
@patch('os.path.exists')
@patch('ara_cli.artefact.Artefact.from_content')  # Mock Artefact.from_content
def test_list_data_file_handling(mock_from_content, mock_exists, mock_list_files_in_directory, mock_artefact_reader, mock_file_classifier, artefact_lister, classifier, artefact_name, content, file_path, does_exist):
    # Mock the Artefact.from_content method to return a mock artefact
    mock_artefact_instance = MagicMock()
    mock_artefact_instance.name = artefact_name.replace('_', ' ')
    mock_from_content.return_value = mock_artefact_instance

    # Mock the FileClassifier and its methods
    mock_classifier_instance = mock_file_classifier.return_value

    mock_artefact = MagicMock()
    mock_artefact.name = artefact_name.replace('_', ' ')
    mock_artefact.file_path = file_path.replace('.data', '')
    mock_classifier_instance.classify_files = MagicMock(return_value={classifier: [mock_artefact]})

    # Mock ArtefactReader's read_artefact method
    mock_artefact_reader.read_artefact = MagicMock(return_value=(content, file_path))

    # Mock os.path.exists
    mock_exists.return_value = does_exist

    # Call the method under test
    artefact_lister.list_data(classifier=classifier, artefact_name=artefact_name)

    # Verify read_artefact was called with the correct parameters
    mock_artefact_reader.read_artefact.assert_called_once_with(classifier=classifier, artefact_name=artefact_name)

    # Verify list_files_in_directory was called if the file exists
    if does_exist:
        mock_list_files_in_directory.assert_called_once_with(file_path, None)
    else:
        mock_list_files_in_directory.assert_not_called()

    # Verify os.path.exists was called with the correct file path
    mock_exists.assert_called_once_with(file_path)
