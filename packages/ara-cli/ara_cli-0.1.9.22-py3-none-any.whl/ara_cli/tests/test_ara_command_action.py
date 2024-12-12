import pytest
from unittest.mock import patch, MagicMock
from ara_cli.ara_command_action import check_validity, create_action, delete_action, rename_action, list_action, reconnect_action


@pytest.fixture
def mock_dependencies():
    with patch('ara_cli.artefact_creator.ArtefactCreator') as MockArtefactCreator, \
         patch('ara_cli.classifier.Classifier') as MockClassifier, \
         patch('ara_cli.filename_validator.is_valid_filename') as mock_is_valid_filename, \
         patch('ara_cli.template_manager.SpecificationBreakdownAspects') as MockSpecificationBreakdownAspects:
        yield MockArtefactCreator, MockClassifier, mock_is_valid_filename, MockSpecificationBreakdownAspects


@pytest.fixture
def mock_reconnect_dependencies():
    with patch('ara_cli.artefact.Artefact') as MockArtefact, \
         patch('ara_cli.artefact_reader.ArtefactReader') as MockArtefactReader, \
         patch('ara_cli.file_classifier.FileClassifier') as MockFileClassifier, \
         patch('ara_cli.directory_navigator.DirectoryNavigator') as MockDirectoryNavigator, \
         patch('ara_cli.ara_command_action.suggest_close_name_matches') as mock_suggest_close_name_matches:
        yield MockArtefact, MockArtefactReader, MockFileClassifier, MockDirectoryNavigator, mock_suggest_close_name_matches


@pytest.fixture
def mock_artefact_deleter():
    with patch('ara_cli.artefact_deleter.ArtefactDeleter') as MockArtefactDeleter:
        yield MockArtefactDeleter


@pytest.fixture
def mock_artefact_renamer():
    with patch('ara_cli.artefact_renamer.ArtefactRenamer') as MockArtefactRenamer, \
         patch('ara_cli.classifier.Classifier') as MockClassifier, \
         patch('ara_cli.filename_validator.is_valid_filename') as mock_is_valid_filename:
        yield MockArtefactRenamer, MockClassifier, mock_is_valid_filename


@pytest.fixture
def mock_artefact_reader():
    with patch('ara_cli.artefact_reader.ArtefactReader') as MockArtefactReader:
        yield MockArtefactReader


@pytest.fixture
def mock_artefact_lister():
    with patch('ara_cli.artefact_lister.ArtefactLister') as MockArtefactLister:
        yield MockArtefactLister


@pytest.fixture
def mock_list_filter():
    with patch('ara_cli.list_filter.ListFilter') as MockListFilter:
        yield MockListFilter


@pytest.fixture
def mock_directory_navigator():
    with patch('ara_cli.directory_navigator.DirectoryNavigator') as MockDirectoryNavigator:
        yield MockDirectoryNavigator


@pytest.fixture
def mock_artefact():
    with patch('ara_cli.artefact.Artefact') as MockArtefact:
        yield MockArtefact


@pytest.mark.parametrize("condition, error_message", [
    (True, "This should not be printed"),
    (False, "This is a test error message")
])
def test_check_validity(condition, error_message):
    with patch('sys.exit') as mock_exit, patch('builtins.print') as mock_print:
        if condition:
            check_validity(condition, error_message)
            mock_exit.assert_not_called()
            mock_print.assert_not_called()
        else:
            check_validity(condition, error_message)
            mock_exit.assert_called_once_with(1)
            mock_print.assert_called_once_with(error_message)


@pytest.mark.parametrize("classifier_valid, filename_valid", [
    (True, True),
    (False, True),
    (True, False),
    (False, False)
])
def test_create_action_validity_checks(mock_dependencies, classifier_valid, filename_valid):
    MockArtefactCreator, MockClassifier, mock_is_valid_filename, MockSpecificationBreakdownAspects = mock_dependencies
    MockClassifier.is_valid_classifier.return_value = classifier_valid
    mock_is_valid_filename.return_value = filename_valid

    args = MagicMock()
    args.classifier = 'test_classifier'
    args.parameter = 'test_parameter'

    with patch('ara_cli.ara_command_action.check_validity') as mock_check_validity:
        if classifier_valid and filename_valid:
            create_action(args)
            mock_check_validity.assert_any_call(True, "Invalid classifier provided. Please provide a valid classifier.")
            mock_check_validity.assert_any_call(True, "Invalid filename provided. Please provide a valid filename.")
        else:
            create_action(args)
            if not classifier_valid:
                mock_check_validity.assert_any_call(False, "Invalid classifier provided. Please provide a valid classifier.")
            if not filename_valid:
                mock_check_validity.assert_any_call(False, "Invalid filename provided. Please provide a valid filename.")


@pytest.mark.parametrize("parameter, classifier, force", [
    ("valid_param", "valid_classifier", True),
    ("valid_param", "valid_classifier", False),
])
def test_delete_action(mock_artefact_deleter, parameter, classifier, force):
    MockArtefactDeleter = mock_artefact_deleter
    instance = MockArtefactDeleter.return_value

    args = MagicMock()
    args.parameter = parameter
    args.classifier = classifier
    args.force = force

    delete_action(args)

    instance.delete.assert_called_once_with(parameter, classifier, force)


@pytest.mark.parametrize("parameter_valid, classifier_valid, aspect_valid", [
    (True, True, True),
    (False, True, True),
    (True, False, True),
    (True, True, False),
    (False, False, False),
])
def test_rename_action_validity_checks(mock_artefact_renamer, parameter_valid, classifier_valid, aspect_valid):
    MockArtefactRenamer, MockClassifier, mock_is_valid_filename = mock_artefact_renamer
    MockClassifier.is_valid_classifier.return_value = classifier_valid
    mock_is_valid_filename.side_effect = [parameter_valid, aspect_valid]

    args = MagicMock()
    args.parameter = 'test_parameter'
    args.classifier = 'test_classifier'
    args.aspect = 'test_aspect'

    with patch('ara_cli.ara_command_action.check_validity') as mock_check_validity:
        if parameter_valid and classifier_valid and aspect_valid:
            rename_action(args)
            mock_check_validity.assert_any_call(True, "Invalid filename provided. Please provide a valid filename.")
            mock_check_validity.assert_any_call(True, "Invalid classifier provided. Please provide a valid classifier.")
            mock_check_validity.assert_any_call(True, "Invalid new filename provided. Please provide a valid filename.")
        else:
            rename_action(args)
            if not parameter_valid:
                mock_check_validity.assert_any_call(False, "Invalid filename provided. Please provide a valid filename.")
            if not classifier_valid:
                mock_check_validity.assert_any_call(False, "Invalid classifier provided. Please provide a valid classifier.")
            if not aspect_valid:
                mock_check_validity.assert_any_call(False, "Invalid new filename provided. Please provide a valid filename.")


@pytest.mark.parametrize("parameter, aspect, classifier", [
    ("valid_param", "new_valid_aspect", "valid_classifier"),
])
def test_rename_action_renamer_call(mock_artefact_renamer, parameter, aspect, classifier):
    MockArtefactRenamer, MockClassifier, mock_is_valid_filename = mock_artefact_renamer
    MockClassifier.is_valid_classifier.return_value = True
    mock_is_valid_filename.return_value = True

    args = MagicMock()
    args.parameter = parameter
    args.classifier = classifier
    args.aspect = aspect

    rename_action(args)
    MockArtefactRenamer.return_value.rename.assert_called_once_with(parameter, aspect, classifier)


@pytest.mark.parametrize("branch_args, children_args, data_args, expected_call", [
    (("branch_classifier", "branch_name"), (None, None), (None, None), "list_branch"),
    ((None, None), ("children_classifier", "children_name"), (None, None), "list_children"),
    ((None, None), (None, None), ("data_classifier", "data_name"), "list_data"),
])
def test_list_action_calls_correct_method(mock_artefact_lister, mock_list_filter, branch_args, children_args, data_args, expected_call):
    MockArtefactLister = mock_artefact_lister
    list_filter_instance = mock_list_filter.return_value

    args = MagicMock()
    args.branch_args = branch_args
    args.children_args = children_args
    args.data_args = data_args
    args.include_content = None
    args.exclude_content = None
    args.include_extension = None
    args.exclude_extension = None

    list_action(args)
    instance = MockArtefactLister.return_value
    getattr(instance, expected_call).assert_called_once_with(
        classifier=branch_args[0] or children_args[0] or data_args[0],
        artefact_name=branch_args[1] or children_args[1] or data_args[1],
        list_filter=list_filter_instance
    )


@pytest.mark.parametrize("include_content, exclude_content, include_extension, exclude_extension", [
    ("text", None, ".txt", None),
    (None, "text", None, ".txt"),
    ("text", "text", ".txt", ".md")
])
def test_list_action_creates_list_filter(mock_artefact_lister, mock_list_filter, include_content, exclude_content, include_extension, exclude_extension):
    mock_list_filter.return_value = MagicMock()

    args = MagicMock()
    args.branch_args = (None, None)
    args.children_args = (None, None)
    args.data_args = (None, None)
    args.include_content = include_content
    args.exclude_content = exclude_content
    args.include_extension = include_extension
    args.exclude_extension = exclude_extension

    list_action(args)
    mock_list_filter.assert_called_once_with(
        include_content=include_content,
        exclude_content=exclude_content,
        include_extension=include_extension,
        exclude_extension=exclude_extension
    )
