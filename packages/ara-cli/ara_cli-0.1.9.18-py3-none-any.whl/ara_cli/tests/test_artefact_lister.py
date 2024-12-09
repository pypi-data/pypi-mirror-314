import pytest
from unittest.mock import MagicMock, patch
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


@pytest.mark.parametrize("classifier, artefact_name", [
    ("classifier1", "artefact1"),
    ("classifier2", "artefact2"),
    ("classifier3", "artefact3"),
])
@patch('ara_cli.artefact_lister.FileClassifier')
@patch('ara_cli.artefact_lister.ArtefactReader')
def test_list_branch(mock_artefact_reader, mock_file_classifier, artefact_lister, classifier, artefact_name):
    # Mock the FileClassifier and its methods
    mock_classifier_instance = mock_file_classifier.return_value
    mock_classifier_instance.print_classified_files = MagicMock()

    # Mock the ArtefactReader and its methods
    mock_artefact_reader.step_through_value_chain = MagicMock()

    # Call the method under test
    artefact_lister.list_branch(classifier=classifier, artefact_name=artefact_name)

    # Verify step_through_value_chain was called with the correct parameters
    mock_artefact_reader.step_through_value_chain.assert_called_once_with(
        artefact_name=artefact_name,
        classifier=classifier,
        artefacts_by_classifier={classifier: []}
    )

    # Verify print_classified_files was called with the correct artefacts_by_classifier
    mock_classifier_instance.print_classified_files.assert_called_once_with({classifier: []})


@pytest.mark.parametrize("classifier, artefact_name, expected_children", [
    ("classifier1", "artefact1", {'mocked_children': []}),
    ("classifier2", "artefact2", {'mocked_children': ['child1', 'child2']}),
    ("classifier3", "artefact3", {'mocked_children': ['child3']}),
])
@patch('ara_cli.artefact_lister.FileClassifier')
@patch('ara_cli.artefact_lister.ArtefactReader')
def test_list_children(mock_artefact_reader, mock_file_classifier, artefact_lister, classifier, artefact_name, expected_children):
    # Mock the FileClassifier and its methods
    mock_classifier_instance = mock_file_classifier.return_value
    mock_classifier_instance.print_classified_files = MagicMock()

    # Mock the ArtefactReader and its methods
    mock_artefact_reader.find_children = MagicMock(return_value=expected_children)

    # Call the method under test
    artefact_lister.list_children(classifier=classifier, artefact_name=artefact_name)

    # Verify find_children was called with the correct parameters
    mock_artefact_reader.find_children.assert_called_once_with(
        artefact_name=artefact_name,
        classifier=classifier
    )

    # Verify print_classified_files was called with the correct child artefacts
    mock_classifier_instance.print_classified_files.assert_called_once_with(
        files_by_classifier=expected_children
    )


@pytest.mark.parametrize("classifier, artefact_name, artefact_content, artefact_path, file_exists", [
    ("classifier1", "artefact1", "content1", "path1", True),
    ("classifier2", "artefact2", "content2", "path2", False),
    ("classifier3", "artefact3", "content3", "path3", True),
])
@patch('ara_cli.artefact_lister.ArtefactReader')
@patch('ara_cli.artefact_lister.FileClassifier')
@patch('ara_cli.artefact_lister.list_files_in_directory')
@patch('os.path.exists')
@patch('os.path.splitext')
def test_list_data(mock_splitext, mock_exists, mock_list_files, mock_file_classifier, mock_artefact_reader, artefact_lister, classifier, artefact_name, artefact_content, artefact_path, file_exists):
    # Mock FileClassifier and its methods
    mock_classifier_instance = mock_file_classifier.return_value
    mock_classifier_instance.classify_files.return_value = {
        classifier: [MagicMock(name=artefact_name, file_path=artefact_path)]
    }

    # Mock ArtefactReader and its methods
    mock_artefact_reader.read_artefact.return_value = (artefact_content, artefact_path)

    # Mock Artefact.from_content
    with patch('ara_cli.artefact.Artefact.from_content', return_value=MagicMock(name=artefact_name)):

        # Mock os methods
        mock_splitext.return_value = (artefact_path, '.ext')
        mock_exists.return_value = file_exists

        # Call the method under test
        artefact_lister.list_data(classifier=classifier, artefact_name=artefact_name)

        # Verify the behavior depending on file existence
        expected_data_path = artefact_path + '.data'
        mock_splitext.assert_called_once()

        if file_exists:
            mock_exists.assert_called_once()
            mock_list_files.assert_called_once()
        else:
            mock_exists.assert_called_once_with(expected_data_path)
            mock_list_files.assert_not_called()
